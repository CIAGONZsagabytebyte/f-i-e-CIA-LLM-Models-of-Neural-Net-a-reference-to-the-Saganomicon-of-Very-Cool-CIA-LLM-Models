"""
Saga 64-Bit System Examples

Comprehensive examples showing:
- 64-bit field encoding
- Quantum qubit representations
- Self-referential logging
- Complete reference tracking
- All 64 units combined

By PAUL RUTHERFORDS
"""

import sys
sys.path.insert(0, '.')

from io_fields.saga_64bit import *
from io_fields import IdentityField
import math


def example_1_64bit_encoding():
    """Example 1: Complete 64-bit field encoding"""
    print("=" * 70)
    print("EXAMPLE 1: 64-Bit Field Encoding")
    print("=" * 70)
    print()

    # Create various field types
    fields = [
        Saga64BitField(SagaFieldType.INTEGER, SagaFlags.IMMUTABLE, 0, 0x0001),
        Saga64BitField(SagaFieldType.FLOAT, SagaFlags.VALIDATED, 1, 0x0002),
        Saga64BitField(SagaFieldType.IDENTITY_FIELD, SagaFlags.COSMIC | SagaFlags.LOGGED, 2, 0x0003),
        Saga64BitField(SagaFieldType.QUANTUM_STATE, SagaFlags.QUANTUM | SagaFlags.ENTANGLED, 3, 0x0004),
    ]

    for i, field in enumerate(fields):
        print(f"Field {i+1}:")
        print(f"  Type: {field.field_type.name}")
        print(f"  Flags: {bin(field.flags)}")
        print(f"  64-bit: 0x{field.to_64bit():016x}")
        print(f"  Binary: {field.to_binary_string()[:32]}...")
        print()

    # Demonstrate round-trip
    print("Round-trip test:")
    original = fields[2]
    bits = original.to_64bit()
    reconstructed = Saga64BitField.from_64bit(bits)
    print(f"  Original:      {original}")
    print(f"  Bits:          0x{bits:016x}")
    print(f"  Reconstructed: {reconstructed}")
    print()


def example_2_quantum_qubits():
    """Example 2: Quantum qubit operations"""
    print("=" * 70)
    print("EXAMPLE 2: Quantum Qubit Representations")
    print("=" * 70)
    print()

    # Create qubits in different states
    print("Basic qubit states:")
    q0 = SagaQubit(1.0, 0.0)  # |0⟩
    q1 = SagaQubit(0.0, 1.0)  # |1⟩
    q_plus = SagaQubit(1/math.sqrt(2), 1/math.sqrt(2))  # |+⟩
    q_minus = SagaQubit(1/math.sqrt(2), -1/math.sqrt(2))  # |-⟩

    for name, qubit in [("  |0⟩", q0), ("  |1⟩", q1), ("  |+⟩", q_plus), ("  |-⟩", q_minus)]:
        print(f"{name}: {qubit}")
        print(f"       P(0)={qubit.probability_0():.3f}, P(1)={qubit.probability_1():.3f}")

    print()

    # Quantum gates
    print("Quantum gate operations:")
    q = SagaQubit(1.0, 0.0)  # Start with |0⟩
    print(f"  Initial:   {q}")

    q_h = q.apply_hadamard()
    print(f"  Hadamard:  {q_h}")

    q_x = q_h.apply_pauli_x()
    print(f"  Pauli-X:   {q_x}")

    q_z = q_h.apply_pauli_z()
    print(f"  Pauli-Z:   {q_z}")

    q_phase = q_h.apply_phase(math.pi / 4)
    print(f"  Phase π/4: {q_phase}")
    print()

    # 64-qubit system
    print("64-qubit quantum system:")
    quantum64 = SagaQuantum64()
    quantum64.encode_64bit(0xDEADBEEFCAFEBABE)
    print(f"  {quantum64}")
    print(f"  State vector (first 8): {quantum64.get_quantum_state_vector()}")

    # Create superposition
    quantum_super = quantum64.apply_hadamard_all()
    print(f"  After Hadamard: {quantum_super}")
    print()


def example_3_self_referential_logging():
    """Example 3: Self-referential logging with hierarchy"""
    print("=" * 70)
    print("EXAMPLE 3: Self-Referential Logging System")
    print("=" * 70)
    print()

    log = SagaSelfRefLog()

    # Create hierarchical log structure
    root = log.enter_context("Saga Transformation Pipeline")

    log.log("Phase 1: Initialize identity field", "INFO")

    transform_ctx = log.enter_context("Phase 2: Apply Transformations")
    log.log("Transform 1: Amplify by φ", "TRANSFORM")
    log.log("Transform 2: Normalize", "TRANSFORM")
    log.log("Transform 3: Apply cosmic resonance", "TRANSFORM")
    log.exit_context()

    validate_ctx = log.enter_context("Phase 3: Validation")
    log.log("Check type preservation", "VALIDATE")
    log.log("Verify checksum", "VALIDATE")
    log.log("Confirm saga property", "VALIDATE")
    log.exit_context()

    log.log("Phase 4: Complete - Result ready", "SUCCESS")

    print("Complete log tree:")
    print(log.get_tree(root))
    print()

    print("Reference chains:")
    for entry_id in [3, 7, 10]:
        if entry_id in log.entries:
            chain = log.get_reference_chain(entry_id)
            chain_str = " -> ".join(f"{id:04x}" for id in reversed(chain))
            print(f"  Entry {entry_id:04x}: {chain_str}")
    print()

    # 64-bit encoding of logs
    print("64-bit encoding of log entries:")
    encoded = log.encode_all_64bit()
    for i, bits in enumerate(encoded[:5]):
        print(f"  Entry {i+1}: 0x{bits:016x}")
    print()


def example_4_reference_graph():
    """Example 4: Complete reference tracking"""
    print("=" * 70)
    print("EXAMPLE 4: Reference Graph Tracking")
    print("=" * 70)
    print()

    graph = SagaReferenceGraph()

    # Build reference graph
    print("Building reference graph...")

    # Add nodes
    for i in range(10):
        graph.add_node(i, f"Node_{i}")

    # Add various reference types
    graph.add_reference(0, 1, "parent-child")
    graph.add_reference(0, 2, "parent-child")
    graph.add_reference(1, 3, "parent-child")
    graph.add_reference(1, 4, "parent-child")
    graph.add_reference(2, 5, "parent-child")
    graph.add_reference(3, 6, "sibling")
    graph.add_reference(4, 6, "sibling")

    # Self-reference
    graph.add_reference(5, 5, "self-ref")

    # Circular reference
    graph.add_reference(6, 7, "circular")
    graph.add_reference(7, 8, "circular")
    graph.add_reference(8, 6, "circular")

    print(f"Graph: {graph}")
    print()

    # Find cycles
    cycles = graph.find_cycles()
    print(f"Cycles found: {len(cycles)}")
    for i, cycle in enumerate(cycles[:5]):
        cycle_str = " -> ".join(f"{n:04x}" for n in cycle)
        print(f"  Cycle {i+1}: {cycle_str}")
    print()

    # Self-referential nodes
    self_ref = graph.get_self_referential_nodes()
    print(f"Self-referential nodes: {[f'{n:04x}' for n in self_ref]}")
    print()

    # DOT export
    print("DOT format (for visualization):")
    dot = graph.to_dot()
    print(dot[:200] + "...")
    print()


def example_5_64_units_combined():
    """Example 5: All 64 units combined"""
    print("=" * 70)
    print("EXAMPLE 5: 64-Unit Combinatorial System")
    print("=" * 70)
    print()

    saga64 = Saga64Units()

    # Add 64 units of various types
    print("Creating 64 units...")
    for i in range(64):
        field_type = SagaFieldType(i % 16)

        # Vary flags based on position
        flags = SagaFlags.NONE
        if i % 2 == 0:
            flags |= SagaFlags.IMMUTABLE
        if i % 3 == 0:
            flags |= SagaFlags.LOGGED
        if i % 5 == 0:
            flags |= SagaFlags.COSMIC
        if i % 7 == 0:
            flags |= SagaFlags.QUANTUM

        generation = i // 8  # 8 generations

        saga64.add_unit(field_type, flags, generation)

    print(f"Created {len(saga64.units)} units")
    print()

    # Get statistics
    stats = saga64.get_statistics()
    print("Statistics:")
    print(f"  Total units: {stats['total_units']}")
    print(f"  Combined 64-bit: 0x{stats['combined_64bit']}")
    print(f"  Log entries: {stats['log_entries']}")
    print()

    print("Type distribution:")
    for type_name, count in sorted(stats['type_distribution'].items()):
        print(f"  {type_name:20s}: {count:3d}")
    print()

    print("Flag distribution:")
    for flag_name, count in sorted(stats['flag_distribution'].items()):
        print(f"  {flag_name:20s}: {count:3d}")
    print()

    # Convert to quantum state
    print("Converting to quantum state...")
    quantum = saga64.to_quantum_state()
    print(f"  {quantum}")
    print()


def example_6_identity_field_64bit():
    """Example 6: Identity Field with 64-bit encoding"""
    print("=" * 70)
    print("EXAMPLE 6: Identity Field + 64-Bit Encoding")
    print("=" * 70)
    print()

    # Create identity field
    I = IdentityField(42)
    print(f"Identity Field: {I}")
    print()

    # Apply transformations
    I2 = I.apply(lambda x: x * 2)
    I3 = I2.apply(lambda x: x + 10)
    I4 = I3.apply(lambda x: x * 1.618)

    print(f"Lineage: {I4.get_lineage()}")
    print()

    # Encode each transformation as 64-bit
    print("64-bit encoding of transformation steps:")
    for i, value in enumerate(I4.get_lineage()):
        field = Saga64BitField(
            field_type=SagaFieldType.IDENTITY_FIELD,
            flags=SagaFlags.TRANSFORMED | SagaFlags.LOGGED,
            generation=i,
            ref_id=hash(str(value)) & 0xFFFF
        )
        print(f"  Step {i}: value={value:10.3f}, 64-bit=0x{field.to_64bit():016x}")
    print()


def example_7_complete_integration():
    """Example 7: Complete integration of all systems"""
    print("=" * 70)
    print("EXAMPLE 7: Complete System Integration")
    print("=" * 70)
    print()

    # Initialize all systems
    saga64 = Saga64Units()
    log = SagaSelfRefLog()
    graph = SagaReferenceGraph()

    print("Creating integrated Saga system...")
    print()

    # Create identity field
    ctx = log.enter_context("Create Identity Field")
    I = IdentityField(100)

    unit_id = saga64.add_unit(
        SagaFieldType.IDENTITY_FIELD,
        SagaFlags.IMMUTABLE | SagaFlags.LOGGED | SagaFlags.COSMIC
    )
    graph.add_node(unit_id, I)
    log.log(f"Created identity field: {I}", "CREATE")
    log.exit_context()

    # Apply transformations
    ctx = log.enter_context("Apply Transformations")

    for i, (name, func) in enumerate([
        ("Golden ratio", lambda x: x * 1.618),
        ("Normalize", lambda x: x / 100),
        ("Square", lambda x: x ** 2)
    ]):
        log.log(f"Applying: {name}", "TRANSFORM")
        I = I.apply(func)

        unit_id_new = saga64.add_unit(
            SagaFieldType.IDENTITY_FIELD,
            SagaFlags.TRANSFORMED | SagaFlags.LOGGED,
            generation=i+1
        )
        graph.add_node(unit_id_new, I)
        graph.add_reference(unit_id, unit_id_new, "transform")
        unit_id = unit_id_new

    log.exit_context()

    # Results
    ctx = log.enter_context("Results")
    log.log(f"Final value: {I.get_identity()}", "RESULT")
    log.log(f"Transformations applied: {len(I._transformations)}", "RESULT")
    log.exit_context()

    print("Log structure:")
    print(log.get_tree(1))
    print()

    print("64-unit statistics:")
    stats = saga64.get_statistics()
    print(f"  Units: {stats['total_units']}")
    print(f"  Combined: 0x{stats['combined_64bit']}")
    print()

    print("Reference graph:")
    print(f"  Nodes: {len(graph.nodes)}")
    print(f"  Edges: {len(graph.edges)}")
    print()

    print("Final identity field:")
    print(f"  Value: {I.get_identity()}")
    print(f"  Lineage: {I.get_lineage()}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("SAGA 64-BIT SYSTEM - COMPLETE EXAMPLES")
    print("By PAUL RUTHERFORDS")
    print("=" * 70 + "\n")

    try:
        example_1_64bit_encoding()
        example_2_quantum_qubits()
        example_3_self_referential_logging()
        example_4_reference_graph()
        example_5_64_units_combined()
        example_6_identity_field_64bit()
        example_7_complete_integration()

        print("=" * 70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY ✨")
        print("=" * 70)
        print()
        print("Summary:")
        print("  ✓ 64-bit field encoding")
        print("  ✓ Quantum qubit representations")
        print("  ✓ Self-referential logging")
        print("  ✓ Reference graph tracking")
        print("  ✓ 64-unit combinatorial system")
        print("  ✓ Identity field integration")
        print("  ✓ Complete system integration")
        print()
        print("i.f(I) = I = f(x) in 64 bits ✨")
        print("=" * 70)

    except Exception as e:
        print(f"\nError in examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
