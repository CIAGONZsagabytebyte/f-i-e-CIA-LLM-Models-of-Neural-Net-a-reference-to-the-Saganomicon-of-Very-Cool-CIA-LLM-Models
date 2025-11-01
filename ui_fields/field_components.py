"""
Field Components - Basic UI field building blocks

Each component maintains field properties and can participate in
saga transformations: i(f(Saga)=i)
"""

from typing import Any, Callable, List, Optional, Dict
import re


class BaseField:
    """Base class for all UI fields"""

    def __init__(self, name: str, label: str = None, initial_value: Any = None):
        self.name = name
        self.label = label or name
        self.value = initial_value
        self.validators = []
        self.transformers = []
        self.observers = []
        self.metadata = {}
        self.valid = True
        self.error_message = None

    def set_value(self, value: Any) -> bool:
        """Set the field value with validation"""
        # Apply transformers
        for transformer in self.transformers:
            value = transformer(value)

        # Validate
        self.valid = True
        self.error_message = None

        for validator in self.validators:
            if not validator(value):
                self.valid = False
                self.error_message = f"Validation failed for {self.name}"
                return False

        # Set value
        self.value = value

        # Notify observers
        self._notify_observers()
        return True

    def get_value(self) -> Any:
        """Get the current field value"""
        return self.value

    def add_validator(self, validator: Callable[[Any], bool]) -> 'BaseField':
        """Add a validation function"""
        self.validators.append(validator)
        return self

    def add_transformer(self, transformer: Callable[[Any], Any]) -> 'BaseField':
        """Add a transformation function (saga field)"""
        self.transformers.append(transformer)
        return self

    def observe(self, observer: Callable[['BaseField'], None]) -> 'BaseField':
        """Add an observer for value changes"""
        self.observers.append(observer)
        return self

    def _notify_observers(self) -> None:
        """Notify all observers of value change"""
        for observer in self.observers:
            try:
                observer(self)
            except Exception as e:
                print(f"Observer error: {e}")

    def reset(self) -> None:
        """Reset to initial state"""
        self.value = None
        self.valid = True
        self.error_message = None

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, value={self.value}, valid={self.valid})"


class TextField(BaseField):
    """Text input field with saga-inspired string transformations"""

    def __init__(self, name: str, label: str = None, initial_value: str = "",
                 max_length: Optional[int] = None, pattern: Optional[str] = None):
        super().__init__(name, label, initial_value)
        self.max_length = max_length
        self.pattern = pattern

        # Add automatic validators
        if max_length:
            self.add_validator(lambda v: len(str(v)) <= max_length)
        if pattern:
            self.add_validator(lambda v: bool(re.match(pattern, str(v))))

    def apply_cosmic_resonance(self) -> str:
        """Apply cosmic resonance transformation to text"""
        if isinstance(self.value, str):
            return f"✨{self.value}✨"
        return str(self.value)

    def to_ascii_art(self) -> str:
        """Convert text to ASCII art representation"""
        if not self.value:
            return ""

        # Simple ASCII art banner
        border = "=" * (len(self.value) + 4)
        return f"{border}\n| {self.value} |\n{border}"


class NumberField(BaseField):
    """Numeric input field with mathematical field operations"""

    def __init__(self, name: str, label: str = None, initial_value: float = 0.0,
                 min_value: Optional[float] = None, max_value: Optional[float] = None,
                 step: float = 1.0):
        super().__init__(name, label, initial_value)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

        # Add range validators
        if min_value is not None:
            self.add_validator(lambda v: float(v) >= min_value)
        if max_value is not None:
            self.add_validator(lambda v: float(v) <= max_value)

    def increment(self) -> bool:
        """Increment by step"""
        new_value = float(self.value) + self.step
        return self.set_value(new_value)

    def decrement(self) -> bool:
        """Decrement by step"""
        new_value = float(self.value) - self.step
        return self.set_value(new_value)

    def apply_golden_ratio(self) -> float:
        """Apply golden ratio transformation"""
        phi = 1.618033988749
        return float(self.value) * phi

    def apply_fibonacci_field(self) -> int:
        """Find the nearest Fibonacci number"""
        n = abs(int(self.value))
        fib_prev, fib_curr = 0, 1

        while fib_curr < n:
            fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

        # Return closest
        if abs(n - fib_prev) < abs(n - fib_curr):
            return fib_prev
        return fib_curr


class SelectField(BaseField):
    """Selection field with discrete options"""

    def __init__(self, name: str, label: str = None, options: List[Any] = None,
                 initial_value: Any = None, multiple: bool = False):
        super().__init__(name, label, initial_value)
        self.options = options or []
        self.multiple = multiple

        # Add validator for valid options
        if not multiple:
            self.add_validator(lambda v: v in self.options)
        else:
            self.add_validator(lambda v: all(item in self.options for item in v))

    def add_option(self, option: Any) -> 'SelectField':
        """Add a new option"""
        if option not in self.options:
            self.options.append(option)
        return self

    def remove_option(self, option: Any) -> 'SelectField':
        """Remove an option"""
        if option in self.options:
            self.options.remove(option)
        return self

    def select_next(self) -> bool:
        """Select next option (cyclic)"""
        if not self.options or self.multiple:
            return False

        try:
            current_index = self.options.index(self.value)
            next_index = (current_index + 1) % len(self.options)
            return self.set_value(self.options[next_index])
        except ValueError:
            return self.set_value(self.options[0])

    def select_previous(self) -> bool:
        """Select previous option (cyclic)"""
        if not self.options or self.multiple:
            return False

        try:
            current_index = self.options.index(self.value)
            prev_index = (current_index - 1) % len(self.options)
            return self.set_value(self.options[prev_index])
        except ValueError:
            return self.set_value(self.options[-1])


class ToggleField(BaseField):
    """Boolean toggle field with state transformations"""

    def __init__(self, name: str, label: str = None, initial_value: bool = False):
        super().__init__(name, label, initial_value)

    def toggle(self) -> bool:
        """Toggle the field value"""
        return self.set_value(not self.value)

    def enable(self) -> bool:
        """Set to True"""
        return self.set_value(True)

    def disable(self) -> bool:
        """Set to False"""
        return self.set_value(False)

    def as_string(self) -> str:
        """Convert to string representation"""
        return "ON" if self.value else "OFF"

    def as_emoji(self) -> str:
        """Convert to emoji representation"""
        return "✅" if self.value else "❌"


class ColorField(BaseField):
    """Color field with solarpunk palette support"""

    SOLARPUNK_PALETTE = {
        'mint': '#64C8B4',
        'lavender': '#B4A0FF',
        'cyan': '#64C8DC',
        'dusty_orange': '#DCA06E',
        'deep_purple': '#19141F',
        'solar_yellow': '#FFD700',
        'forest_green': '#228B22',
        'cosmic_blue': '#4B0082'
    }

    def __init__(self, name: str, label: str = None, initial_value: str = '#000000'):
        super().__init__(name, label, initial_value)

        # Validate hex color format
        self.add_validator(self._is_valid_hex_color)

    @staticmethod
    def _is_valid_hex_color(value: str) -> bool:
        """Validate hex color format"""
        if not isinstance(value, str):
            return False
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', value))

    def set_solarpunk_color(self, color_name: str) -> bool:
        """Set to a solarpunk palette color"""
        if color_name in self.SOLARPUNK_PALETTE:
            return self.set_value(self.SOLARPUNK_PALETTE[color_name])
        return False

    def to_rgb(self) -> tuple[int, int, int]:
        """Convert hex to RGB tuple"""
        hex_color = self.value.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def to_hsl(self) -> tuple[float, float, float]:
        """Convert to HSL (simplified)"""
        r, g, b = self.to_rgb()
        r, g, b = r/255.0, g/255.0, b/255.0

        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2

        if max_c == min_c:
            h = s = 0
        else:
            diff = max_c - min_c
            s = diff / (2 - max_c - min_c) if l > 0.5 else diff / (max_c + min_c)

            if max_c == r:
                h = ((g - b) / diff + (6 if g < b else 0)) / 6
            elif max_c == g:
                h = ((b - r) / diff + 2) / 6
            else:
                h = ((r - g) / diff + 4) / 6

        return (h * 360, s * 100, l * 100)

    def brighten(self, factor: float = 1.2) -> bool:
        """Brighten the color"""
        r, g, b = self.to_rgb()
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        new_hex = f"#{r:02x}{g:02x}{b:02x}"
        return self.set_value(new_hex)

    def darken(self, factor: float = 0.8) -> bool:
        """Darken the color"""
        return self.brighten(factor)
