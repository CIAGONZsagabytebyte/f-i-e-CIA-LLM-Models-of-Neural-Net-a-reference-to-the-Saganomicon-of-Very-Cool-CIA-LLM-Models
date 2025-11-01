"""
Field Validators - Validation chains for UI fields

Implements saga-aware validation that ensures data integrity
while maintaining the i(f(Saga)=i) property.
"""

from typing import Any, Callable, List, Optional, Dict
import re


class FieldValidator:
    """Base validator with common validation patterns"""

    @staticmethod
    def required(value: Any) -> bool:
        """Validate that value is not None or empty"""
        if value is None:
            return False
        if isinstance(value, str) and len(value.strip()) == 0:
            return False
        return True

    @staticmethod
    def min_length(min_len: int) -> Callable[[Any], bool]:
        """Create a minimum length validator"""
        def validator(value: Any) -> bool:
            return len(str(value)) >= min_len
        return validator

    @staticmethod
    def max_length(max_len: int) -> Callable[[Any], bool]:
        """Create a maximum length validator"""
        def validator(value: Any) -> bool:
            return len(str(value)) <= max_len
        return validator

    @staticmethod
    def range_validator(min_val: float, max_val: float) -> Callable[[Any], bool]:
        """Create a range validator for numbers"""
        def validator(value: Any) -> bool:
            try:
                num = float(value)
                return min_val <= num <= max_val
            except (ValueError, TypeError):
                return False
        return validator

    @staticmethod
    def regex_validator(pattern: str) -> Callable[[str], bool]:
        """Create a regex pattern validator"""
        compiled = re.compile(pattern)
        def validator(value: str) -> bool:
            return bool(compiled.match(str(value)))
        return validator

    @staticmethod
    def email_validator(value: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(value)))

    @staticmethod
    def url_validator(value: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, str(value)))

    @staticmethod
    def numeric_validator(value: Any) -> bool:
        """Validate that value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def integer_validator(value: Any) -> bool:
        """Validate that value is an integer"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def positive_validator(value: Any) -> bool:
        """Validate that value is positive"""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def non_negative_validator(value: Any) -> bool:
        """Validate that value is non-negative"""
        try:
            return float(value) >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def one_of(options: List[Any]) -> Callable[[Any], bool]:
        """Create a validator that checks if value is in options"""
        def validator(value: Any) -> bool:
            return value in options
        return validator

    @staticmethod
    def custom(func: Callable[[Any], bool], error_message: str = None) -> Callable[[Any], bool]:
        """Create a custom validator"""
        return func


class ValidationChain:
    """Chain multiple validators together"""

    def __init__(self, name: str = "validation_chain"):
        self.name = name
        self.validators = []
        self.error_messages = []

    def add(self, validator: Callable[[Any], bool], error_message: str = None) -> 'ValidationChain':
        """Add a validator to the chain"""
        self.validators.append(validator)
        self.error_messages.append(error_message or "Validation failed")
        return self

    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Run all validators in the chain
        Returns (is_valid, error_message)
        """
        for validator, error_msg in zip(self.validators, self.error_messages):
            if not validator(value):
                return False, error_msg
        return True, None

    def __call__(self, value: Any) -> bool:
        """Allow chain to be called as a function"""
        is_valid, _ = self.validate(value)
        return is_valid

    def __repr__(self):
        return f"ValidationChain(name={self.name}, validators={len(self.validators)})"


class SagaValidator:
    """
    Saga-aware validator that ensures the i(f(Saga)=i) property
    Validates that transformations preserve essential data properties
    """

    def __init__(self, name: str = "saga_validator"):
        self.name = name
        self.type_checks = True
        self.structure_checks = True
        self.value_constraints = []

    def enable_type_checking(self) -> 'SagaValidator':
        """Enable type preservation checking"""
        self.type_checks = True
        return self

    def disable_type_checking(self) -> 'SagaValidator':
        """Disable type preservation checking"""
        self.type_checks = False
        return self

    def enable_structure_checking(self) -> 'SagaValidator':
        """Enable structure preservation checking"""
        self.structure_checks = True
        return self

    def disable_structure_checking(self) -> 'SagaValidator':
        """Disable structure preservation checking"""
        self.structure_checks = False
        return self

    def add_constraint(self, constraint: Callable[[Any, Any], bool],
                      error_message: str = None) -> 'SagaValidator':
        """
        Add a constraint function that takes (original, transformed) and returns bool
        Example: lambda orig, trans: len(orig) == len(trans)
        """
        self.value_constraints.append({
            'func': constraint,
            'message': error_message or "Constraint violation"
        })
        return self

    def validate_transformation(self, original: Any, transformed: Any) -> tuple[bool, List[str]]:
        """
        Validate that a transformation preserves saga properties
        Returns (is_valid, [error_messages])
        """
        errors = []

        # Type checking
        if self.type_checks:
            if type(original) != type(transformed):
                errors.append(f"Type changed: {type(original).__name__} -> {type(transformed).__name__}")

        # Structure checking for collections
        if self.structure_checks:
            if isinstance(original, dict) and isinstance(transformed, dict):
                if set(original.keys()) != set(transformed.keys()):
                    errors.append("Dictionary keys changed")

            elif isinstance(original, (list, tuple)) and isinstance(transformed, (list, tuple)):
                if len(original) != len(transformed):
                    errors.append(f"Collection length changed: {len(original)} -> {len(transformed)}")

        # Custom constraints
        for constraint in self.value_constraints:
            try:
                if not constraint['func'](original, transformed):
                    errors.append(constraint['message'])
            except Exception as e:
                errors.append(f"Constraint error: {e}")

        return len(errors) == 0, errors

    def create_saga_transform_wrapper(self, transform: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """
        Wrap a transformation function with saga validation
        If validation fails, returns original value
        """
        def wrapped(value: Any) -> Any:
            transformed = transform(value)
            is_valid, errors = self.validate_transformation(value, transformed)

            if is_valid:
                return transformed
            else:
                print(f"Saga validation failed: {', '.join(errors)}")
                return value  # Return original to preserve saga property

        return wrapped

    def __repr__(self):
        return f"SagaValidator(name={self.name}, constraints={len(self.value_constraints)})"


class CompositeValidator:
    """Combine multiple validation strategies"""

    def __init__(self, name: str = "composite"):
        self.name = name
        self.validators = []
        self.mode = 'all'  # 'all' = AND, 'any' = OR

    def add_validator(self, validator: Callable[[Any], bool]) -> 'CompositeValidator':
        """Add a validator"""
        self.validators.append(validator)
        return self

    def set_mode_all(self) -> 'CompositeValidator':
        """Require all validators to pass (AND)"""
        self.mode = 'all'
        return self

    def set_mode_any(self) -> 'CompositeValidator':
        """Require at least one validator to pass (OR)"""
        self.mode = 'any'
        return self

    def validate(self, value: Any) -> bool:
        """Run validation"""
        if not self.validators:
            return True

        if self.mode == 'all':
            return all(validator(value) for validator in self.validators)
        else:  # mode == 'any'
            return any(validator(value) for validator in self.validators)

    def __call__(self, value: Any) -> bool:
        """Allow composite to be called as a function"""
        return self.validate(value)

    def __repr__(self):
        return f"CompositeValidator(name={self.name}, mode={self.mode}, validators={len(self.validators)})"


# Predefined validation chains for common use cases

def create_username_validator() -> ValidationChain:
    """Create a validator for usernames"""
    return ValidationChain("username") \
        .add(FieldValidator.required, "Username is required") \
        .add(FieldValidator.min_length(3), "Username must be at least 3 characters") \
        .add(FieldValidator.max_length(20), "Username must be at most 20 characters") \
        .add(FieldValidator.regex_validator(r'^[a-zA-Z0-9_]+$'), "Username can only contain letters, numbers, and underscores")


def create_password_validator() -> ValidationChain:
    """Create a validator for passwords"""
    return ValidationChain("password") \
        .add(FieldValidator.required, "Password is required") \
        .add(FieldValidator.min_length(8), "Password must be at least 8 characters") \
        .add(lambda p: any(c.isupper() for c in str(p)), "Password must contain an uppercase letter") \
        .add(lambda p: any(c.islower() for c in str(p)), "Password must contain a lowercase letter") \
        .add(lambda p: any(c.isdigit() for c in str(p)), "Password must contain a digit")


def create_email_validator() -> ValidationChain:
    """Create a validator for email addresses"""
    return ValidationChain("email") \
        .add(FieldValidator.required, "Email is required") \
        .add(FieldValidator.email_validator, "Invalid email format")


def create_url_validator() -> ValidationChain:
    """Create a validator for URLs"""
    return ValidationChain("url") \
        .add(FieldValidator.required, "URL is required") \
        .add(FieldValidator.url_validator, "Invalid URL format")


def create_cosmic_coordinate_validator() -> ValidationChain:
    """Create a validator for cosmic coordinates (x, y, z)"""
    return ValidationChain("cosmic_coords") \
        .add(lambda v: isinstance(v, (list, tuple)), "Coordinates must be a list or tuple") \
        .add(lambda v: len(v) == 3, "Coordinates must have exactly 3 values") \
        .add(lambda v: all(isinstance(x, (int, float)) for x in v), "Coordinates must be numeric")
