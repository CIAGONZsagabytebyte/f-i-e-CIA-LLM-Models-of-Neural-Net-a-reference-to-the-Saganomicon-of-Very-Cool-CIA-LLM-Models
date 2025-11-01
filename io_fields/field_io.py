"""
Field I/O - Read and write data through field-based interfaces

Implements persistent field storage and retrieval with cosmic encoding.
"""

import json
import pickle
from typing import Any, Dict, List, Optional
from pathlib import Path
import struct
import hashlib


class FieldReader:
    """Read data from field-encoded sources"""

    def __init__(self, source_path: Optional[str] = None):
        self.source_path = Path(source_path) if source_path else None
        self.field_cache = {}

    def read_json_field(self, path: str) -> Dict[str, Any]:
        """Read a JSON field file"""
        field_path = Path(path)
        if not field_path.exists():
            return {}

        with open(field_path, 'r') as f:
            data = json.load(f)
            self.field_cache[path] = data
            return data

    def read_binary_field(self, path: str) -> bytes:
        """Read a binary field file"""
        field_path = Path(path)
        if not field_path.exists():
            return b''

        with open(field_path, 'rb') as f:
            return f.read()

    def read_saga_field(self, path: str) -> Any:
        """Read a pickled saga field (Python objects)"""
        field_path = Path(path)
        if not field_path.exists():
            return None

        with open(field_path, 'rb') as f:
            return pickle.load(f)

    def stream_lines(self, path: str):
        """Stream lines from a field file (generator)"""
        field_path = Path(path)
        if not field_path.exists():
            return

        with open(field_path, 'r') as f:
            for line in f:
                yield line.strip()

    def read_with_checksum(self, path: str) -> tuple[bytes, str]:
        """Read field data with integrity checksum"""
        data = self.read_binary_field(path)
        checksum = hashlib.sha256(data).hexdigest()
        return data, checksum


class FieldWriter:
    """Write data to field-encoded destinations"""

    def __init__(self, destination_path: Optional[str] = None):
        self.destination_path = Path(destination_path) if destination_path else Path('.')
        self.write_log = []

    def write_json_field(self, path: str, data: Dict[str, Any], indent: int = 2) -> bool:
        """Write data to a JSON field file"""
        try:
            field_path = self.destination_path / path
            field_path.parent.mkdir(parents=True, exist_ok=True)

            with open(field_path, 'w') as f:
                json.dump(data, f, indent=indent)

            self.write_log.append({'path': str(field_path), 'type': 'json', 'success': True})
            return True
        except Exception as e:
            self.write_log.append({'path': str(path), 'type': 'json', 'success': False, 'error': str(e)})
            return False

    def write_binary_field(self, path: str, data: bytes) -> bool:
        """Write binary data to a field file"""
        try:
            field_path = self.destination_path / path
            field_path.parent.mkdir(parents=True, exist_ok=True)

            with open(field_path, 'wb') as f:
                f.write(data)

            self.write_log.append({'path': str(field_path), 'type': 'binary', 'success': True})
            return True
        except Exception as e:
            self.write_log.append({'path': str(path), 'type': 'binary', 'success': False, 'error': str(e)})
            return False

    def write_saga_field(self, path: str, data: Any) -> bool:
        """Write a saga field (pickled Python object)"""
        try:
            field_path = self.destination_path / path
            field_path.parent.mkdir(parents=True, exist_ok=True)

            with open(field_path, 'wb') as f:
                pickle.dump(data, f)

            self.write_log.append({'path': str(field_path), 'type': 'saga', 'success': True})
            return True
        except Exception as e:
            self.write_log.append({'path': str(path), 'type': 'saga', 'success': False, 'error': str(e)})
            return False

    def append_field_line(self, path: str, line: str) -> bool:
        """Append a line to a field file"""
        try:
            field_path = self.destination_path / path
            field_path.parent.mkdir(parents=True, exist_ok=True)

            with open(field_path, 'a') as f:
                f.write(line + '\n')

            return True
        except Exception as e:
            return False

    def write_with_checksum(self, path: str, data: bytes) -> tuple[bool, str]:
        """Write field data with integrity checksum"""
        checksum = hashlib.sha256(data).hexdigest()
        success = self.write_binary_field(path, data)

        if success:
            # Write checksum file
            checksum_path = f"{path}.sha256"
            self.write_binary_field(checksum_path, checksum.encode())

        return success, checksum


class BinaryFieldCodec:
    """Encode and decode data in custom binary field formats"""

    @staticmethod
    def encode_saga_packet(data: Dict[str, Any]) -> bytes:
        """
        Encode a saga packet: [magic][version][length][data][checksum]
        Magic: b'SAGA' (4 bytes)
        Version: uint16 (2 bytes)
        Length: uint32 (4 bytes)
        Data: JSON bytes
        Checksum: SHA256 (32 bytes)
        """
        magic = b'SAGA'
        version = struct.pack('H', 1)  # Version 1

        json_data = json.dumps(data).encode('utf-8')
        length = struct.pack('I', len(json_data))

        checksum = hashlib.sha256(json_data).digest()

        return magic + version + length + json_data + checksum

    @staticmethod
    def decode_saga_packet(packet: bytes) -> Optional[Dict[str, Any]]:
        """Decode a saga packet"""
        if len(packet) < 42:  # Minimum size
            return None

        # Check magic
        if packet[:4] != b'SAGA':
            return None

        # Extract version
        version = struct.unpack('H', packet[4:6])[0]

        # Extract length
        length = struct.unpack('I', packet[6:10])[0]

        # Extract data
        json_data = packet[10:10+length]

        # Extract and verify checksum
        stored_checksum = packet[10+length:10+length+32]
        computed_checksum = hashlib.sha256(json_data).digest()

        if stored_checksum != computed_checksum:
            print("Warning: Checksum mismatch in saga packet")
            return None

        # Decode JSON
        try:
            return json.loads(json_data.decode('utf-8'))
        except:
            return None

    @staticmethod
    def encode_field_array(data: List[float]) -> bytes:
        """Encode a float array in binary format"""
        return struct.pack(f'{len(data)}f', *data)

    @staticmethod
    def decode_field_array(data: bytes) -> List[float]:
        """Decode a float array from binary format"""
        num_floats = len(data) // 4
        return list(struct.unpack(f'{num_floats}f', data))

    @staticmethod
    def encode_cosmic_string(text: str) -> bytes:
        """
        Encode a string with cosmic markers
        Format: [marker][length][utf8_data][marker]
        """
        marker = b'\x9f\x8c\x8c'  # 🌌 emoji bytes
        utf8_data = text.encode('utf-8')
        length = struct.pack('I', len(utf8_data))
        return marker + length + utf8_data + marker

    @staticmethod
    def decode_cosmic_string(data: bytes) -> Optional[str]:
        """Decode a cosmic string"""
        marker = b'\x9f\x8c\x8c'

        if not data.startswith(marker) or not data.endswith(marker):
            return None

        length = struct.unpack('I', data[3:7])[0]
        utf8_data = data[7:7+length]

        try:
            return utf8_data.decode('utf-8')
        except:
            return None
