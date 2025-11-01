"""
Composite Fields - Complex UI structures built from field compositions

Implements higher-order field structures that contain and coordinate
multiple child fields in saga-inspired patterns.
"""

from typing import Any, Dict, List, Optional
from .field_components import BaseField


class FormField:
    """A composite form containing multiple fields"""

    def __init__(self, name: str, title: str = None):
        self.name = name
        self.title = title or name
        self.fields = {}
        self.field_order = []
        self.submit_handlers = []

    def add_field(self, field: BaseField) -> 'FormField':
        """Add a field to the form"""
        self.fields[field.name] = field
        self.field_order.append(field.name)
        return self

    def remove_field(self, field_name: str) -> 'FormField':
        """Remove a field from the form"""
        if field_name in self.fields:
            del self.fields[field_name]
            self.field_order.remove(field_name)
        return self

    def get_field(self, field_name: str) -> Optional[BaseField]:
        """Get a specific field"""
        return self.fields.get(field_name)

    def get_values(self) -> Dict[str, Any]:
        """Get all field values as a dictionary"""
        return {name: field.get_value() for name, field in self.fields.items()}

    def set_values(self, values: Dict[str, Any]) -> bool:
        """Set multiple field values"""
        success = True
        for name, value in values.items():
            if name in self.fields:
                if not self.fields[name].set_value(value):
                    success = False
        return success

    def validate(self) -> bool:
        """Validate all fields"""
        return all(field.valid for field in self.fields.values())

    def reset(self) -> None:
        """Reset all fields"""
        for field in self.fields.values():
            field.reset()

    def on_submit(self, handler: callable) -> 'FormField':
        """Add a submit handler"""
        self.submit_handlers.append(handler)
        return self

    def submit(self) -> bool:
        """Submit the form (validate and call handlers)"""
        if not self.validate():
            return False

        values = self.get_values()
        for handler in self.submit_handlers:
            try:
                handler(values)
            except Exception as e:
                print(f"Submit handler error: {e}")
                return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Export form structure and values"""
        return {
            'name': self.name,
            'title': self.title,
            'fields': {
                name: {
                    'type': field.__class__.__name__,
                    'value': field.get_value(),
                    'valid': field.valid,
                    'label': field.label
                }
                for name, field in self.fields.items()
            },
            'valid': self.validate()
        }

    def __repr__(self):
        return f"FormField(name={self.name}, fields={len(self.fields)}, valid={self.validate()})"


class TableField:
    """A table field with rows and columns of data"""

    def __init__(self, name: str, columns: List[str]):
        self.name = name
        self.columns = columns
        self.rows = []
        self.selected_row = None

    def add_row(self, row_data: Dict[str, Any]) -> 'TableField':
        """Add a row to the table"""
        # Validate columns
        if not all(col in row_data for col in self.columns):
            raise ValueError("Row data must contain all columns")

        self.rows.append(row_data)
        return self

    def remove_row(self, index: int) -> 'TableField':
        """Remove a row by index"""
        if 0 <= index < len(self.rows):
            del self.rows[index]
            if self.selected_row == index:
                self.selected_row = None
        return self

    def update_row(self, index: int, row_data: Dict[str, Any]) -> bool:
        """Update a row"""
        if 0 <= index < len(self.rows):
            self.rows[index].update(row_data)
            return True
        return False

    def get_row(self, index: int) -> Optional[Dict[str, Any]]:
        """Get a row by index"""
        if 0 <= index < len(self.rows):
            return self.rows[index]
        return None

    def select_row(self, index: int) -> bool:
        """Select a row"""
        if 0 <= index < len(self.rows):
            self.selected_row = index
            return True
        return False

    def get_selected_row(self) -> Optional[Dict[str, Any]]:
        """Get the currently selected row"""
        if self.selected_row is not None:
            return self.get_row(self.selected_row)
        return None

    def sort_by_column(self, column: str, reverse: bool = False) -> 'TableField':
        """Sort rows by column"""
        if column in self.columns:
            self.rows.sort(key=lambda row: row.get(column, 0), reverse=reverse)
        return self

    def filter_rows(self, predicate: callable) -> List[Dict[str, Any]]:
        """Filter rows by predicate"""
        return [row for row in self.rows if predicate(row)]

    def to_csv(self) -> str:
        """Export table as CSV"""
        lines = [','.join(self.columns)]
        for row in self.rows:
            values = [str(row.get(col, '')) for col in self.columns]
            lines.append(','.join(values))
        return '\n'.join(lines)

    def __repr__(self):
        return f"TableField(name={self.name}, rows={len(self.rows)}, cols={len(self.columns)})"


class GridField:
    """A 2D grid of cells with field properties"""

    def __init__(self, name: str, width: int, height: int, default_value: Any = None):
        self.name = name
        self.width = width
        self.height = height
        self.grid = [[default_value for _ in range(width)] for _ in range(height)]
        self.selected_cell = None

    def set_cell(self, x: int, y: int, value: Any) -> bool:
        """Set a cell value"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
            return True
        return False

    def get_cell(self, x: int, y: int) -> Optional[Any]:
        """Get a cell value"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def select_cell(self, x: int, y: int) -> bool:
        """Select a cell"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.selected_cell = (x, y)
            return True
        return False

    def get_row(self, y: int) -> Optional[List[Any]]:
        """Get an entire row"""
        if 0 <= y < self.height:
            return self.grid[y].copy()
        return None

    def get_column(self, x: int) -> Optional[List[Any]]:
        """Get an entire column"""
        if 0 <= x < self.width:
            return [self.grid[y][x] for y in range(self.height)]
        return None

    def fill(self, value: Any) -> 'GridField':
        """Fill entire grid with value"""
        self.grid = [[value for _ in range(self.width)] for _ in range(self.height)]
        return self

    def map_cells(self, func: callable) -> 'GridField':
        """Apply function to all cells"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = func(self.grid[y][x], x, y)
        return self

    def get_neighbors(self, x: int, y: int, diagonal: bool = False) -> List[tuple]:
        """Get neighboring cell coordinates"""
        neighbors = []
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if diagonal:
            deltas.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))

        return neighbors

    def to_string(self, separator: str = ' ') -> str:
        """Convert grid to string representation"""
        lines = []
        for row in self.grid:
            line = separator.join(str(cell) for cell in row)
            lines.append(line)
        return '\n'.join(lines)

    def __repr__(self):
        return f"GridField(name={self.name}, size={self.width}x{self.height})"


class FlowField:
    """
    A flow field that directs data through a 2D space
    Inspired by vector fields and particle flows in cosmic space
    """

    def __init__(self, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height
        # Each cell contains (dx, dy) flow vector
        self.vectors = [[(0.0, 0.0) for _ in range(width)] for _ in range(height)]

    def set_vector(self, x: int, y: int, dx: float, dy: float) -> bool:
        """Set flow vector at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.vectors[y][x] = (dx, dy)
            return True
        return False

    def get_vector(self, x: int, y: int) -> Optional[tuple]:
        """Get flow vector at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.vectors[y][x]
        return None

    def create_vortex(self, center_x: float, center_y: float, strength: float = 1.0) -> 'FlowField':
        """Create a vortex flow pattern"""
        for y in range(self.height):
            for x in range(self.width):
                # Vector from cell to center
                dx = center_x - x
                dy = center_y - y

                # Distance
                dist = (dx*dx + dy*dy) ** 0.5
                if dist > 0:
                    # Perpendicular vector (rotated 90 degrees) for vortex
                    vx = -dy / dist * strength
                    vy = dx / dist * strength
                    self.vectors[y][x] = (vx, vy)

        return self

    def create_radial(self, center_x: float, center_y: float, strength: float = 1.0) -> 'FlowField':
        """Create a radial flow pattern (expansion or contraction)"""
        for y in range(self.height):
            for x in range(self.width):
                dx = x - center_x
                dy = y - center_y

                dist = (dx*dx + dy*dy) ** 0.5
                if dist > 0:
                    vx = (dx / dist) * strength
                    vy = (dy / dist) * strength
                    self.vectors[y][x] = (vx, vy)

        return self

    def create_perlin_noise_field(self, scale: float = 0.1, seed: int = 42) -> 'FlowField':
        """Create flow field based on Perlin-like noise"""
        import random
        random.seed(seed)

        for y in range(self.height):
            for x in range(self.width):
                # Simple pseudo-noise
                angle = (random.random() * 2 * 3.14159) * scale
                magnitude = random.random()
                vx = magnitude * (angle % 1.0)
                vy = magnitude * ((angle * 1.7) % 1.0)
                self.vectors[y][x] = (vx, vy)

        return self

    def sample_at(self, x: float, y: float) -> tuple[float, float]:
        """Sample flow vector at fractional position (bilinear interpolation)"""
        x0, y0 = int(x), int(y)
        x1, y1 = min(x0 + 1, self.width - 1), min(y0 + 1, self.height - 1)

        fx, fy = x - x0, y - y0

        # Get corner vectors
        v00 = self.get_vector(x0, y0) or (0, 0)
        v10 = self.get_vector(x1, y0) or (0, 0)
        v01 = self.get_vector(x0, y1) or (0, 0)
        v11 = self.get_vector(x1, y1) or (0, 0)

        # Bilinear interpolation
        vx = (1-fx) * (1-fy) * v00[0] + fx * (1-fy) * v10[0] + \
             (1-fx) * fy * v01[0] + fx * fy * v11[0]
        vy = (1-fx) * (1-fy) * v00[1] + fx * (1-fy) * v10[1] + \
             (1-fx) * fy * v01[1] + fx * fy * v11[1]

        return (vx, vy)

    def trace_particle(self, start_x: float, start_y: float, steps: int = 100, dt: float = 0.1) -> List[tuple]:
        """Trace a particle through the flow field"""
        path = [(start_x, start_y)]
        x, y = start_x, start_y

        for _ in range(steps):
            vx, vy = self.sample_at(x, y)
            x += vx * dt
            y += vy * dt

            # Boundary check
            if not (0 <= x < self.width and 0 <= y < self.height):
                break

            path.append((x, y))

        return path

    def __repr__(self):
        return f"FlowField(name={self.name}, size={self.width}x{self.height})"
