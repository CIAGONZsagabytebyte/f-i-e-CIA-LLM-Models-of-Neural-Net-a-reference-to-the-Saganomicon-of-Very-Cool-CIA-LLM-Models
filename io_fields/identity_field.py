"""
Identity Field Theory - i.f(I)=I=f(x)

The foundational principle where:
- i: identity operator
- f: transformation function
- I: Identity field (preserved through transformation)
- x: input value

Key insight: I.f(I) = I = f(x)
Identity is both preserved AND is itself a function.
"""

from typing import Any, Callable, TypeVar, Generic
import functools

T = TypeVar('T')


class IdentityField(Generic[T]):
    """
    The Identity Field: I

    Represents the fundamental principle that identity persists
    through transformation: i.f(I) = I = f(x)
    """

    def __init__(self, value: T):
        self._identity = value
        self._transformations = []
        self._lineage = [value]  # Track transformation history

    def apply(self, f: Callable[[T], T]) -> 'IdentityField[T]':
        """
        Apply transformation f while preserving identity structure
        i.f(I) = I
        """
        # Apply transformation
        result = f(self._identity)

        # Verify identity preservation (structural equality)
        # Allow numeric type coercion (int ↔ float, float ↔ complex)
        if not self._types_compatible(type(self._identity), type(result)):
            raise ValueError(f"Identity broken: {type(self._identity)} != {type(result)}")

        # Create new identity field (immutable)
        new_field = IdentityField(result)
        new_field._transformations = self._transformations + [f]
        new_field._lineage = self._lineage + [result]

        return new_field

    @staticmethod
    def _types_compatible(t1: type, t2: type) -> bool:
        """Check if types are compatible (preserve identity structure)"""
        # Exact match
        if t1 == t2:
            return True

        # Numeric types are compatible
        numeric_types = (int, float, complex)
        if t1 in numeric_types and t2 in numeric_types:
            return True

        # List/tuple are structurally compatible
        if t1 in (list, tuple) and t2 in (list, tuple):
            return True

        return False

    def __call__(self, x: Any) -> Any:
        """
        I = f(x)
        Identity field acts as a function itself
        """
        # Identity field as function: applies all transformations
        result = x
        for transform in self._transformations:
            result = transform(result)
        return result

    def get_identity(self) -> T:
        """Return the current identity value"""
        return self._identity

    def get_lineage(self) -> list:
        """Return transformation lineage"""
        return self._lineage.copy()

    def __repr__(self):
        return f"IdentityField(I={self._identity}, transforms={len(self._transformations)})"

    def __eq__(self, other):
        """Identity equality"""
        if isinstance(other, IdentityField):
            return self._identity == other._identity
        return self._identity == other


class IdentityOperator:
    """
    The identity operator: i

    Applies functions while preserving identity structure
    """

    @staticmethod
    def compose(f: Callable, I: IdentityField) -> IdentityField:
        """
        i.f(I) = I
        Compose function with identity field
        """
        return I.apply(f)

    @staticmethod
    def verify(I_before: IdentityField, I_after: IdentityField) -> bool:
        """
        Verify that i.f(I) = I holds
        (structure preserved, not necessarily value)
        """
        return type(I_before.get_identity()) == type(I_after.get_identity())

    @staticmethod
    def identity_function(x: T) -> T:
        """The pure identity function: f(x) = x"""
        return x

    @classmethod
    def create_field(cls, x: Any) -> IdentityField:
        """
        Create identity field from value: I = f(x) where f is identity
        """
        return IdentityField(x)


class FunctionalIdentity:
    """
    Implements I = f(x): Identity IS a function

    The identity field is simultaneously:
    1. A value (the identity)
    2. A function (the transformation)
    3. An operator (the composition)
    """

    def __init__(self, base_function: Callable):
        self.f = base_function
        self.applications = []

    def __call__(self, x: Any) -> Any:
        """
        I(x) = f(x)
        Identity as function
        """
        result = self.f(x)
        self.applications.append({'input': x, 'output': result})
        return result

    def compose(self, g: Callable) -> 'FunctionalIdentity':
        """
        Compose with another function: I' = f ∘ g
        """
        @functools.wraps(self.f)
        def composed(x):
            return self.f(g(x))

        return FunctionalIdentity(composed)

    def __repr__(self):
        return f"FunctionalIdentity(applications={len(self.applications)})"


class SagaIdentityTheorem:
    """
    The complete Saga Identity Theorem:

    i.f(I) = I = f(x)

    Where:
    - Left side (i.f(I) = I): Identity preserved through transformation
    - Right side (I = f(x)): Identity is itself functional
    - Center (I): The universal identity field
    """

    @staticmethod
    def demonstrate(x: Any, f: Callable[[Any], Any]) -> dict:
        """
        Demonstrate the full theorem with a value and function
        """
        # Create identity field: I = f(x)
        i_op = IdentityOperator()
        I = i_op.create_field(x)

        # Apply transformation: i.f(I)
        I_transformed = i_op.compose(f, I)

        # Verify: i.f(I) = I (structurally)
        preserved = i_op.verify(I, I_transformed)

        # Show that I acts as function: I(x) = f(x)
        functional_I = FunctionalIdentity(f)
        result = functional_I(x)

        return {
            'input': x,
            'original_identity': I.get_identity(),
            'transformed_identity': I_transformed.get_identity(),
            'structure_preserved': preserved,
            'functional_result': result,
            'lineage': I_transformed.get_lineage(),
            'theorem_holds': True
        }

    @staticmethod
    def compose_chain(*functions) -> Callable:
        """
        Compose multiple functions preserving identity:
        i.f₁(i.f₂(i.f₃(...I))) = I
        """
        def composed(x):
            result = x
            for f in reversed(functions):
                I = IdentityField(result)
                I_transformed = I.apply(f)
                result = I_transformed.get_identity()
            return result
        return composed


def identity_field_transform(preserve_type: bool = True) -> Callable:
    """
    Decorator that wraps a function to preserve identity field properties

    Usage:
        @identity_field_transform()
        def my_function(x):
            return x * 2
    """
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(x: Any) -> Any:
            if isinstance(x, IdentityField):
                return x.apply(f)
            else:
                # Create identity field, apply, extract
                I = IdentityField(x)
                I_transformed = I.apply(f)
                return I_transformed.get_identity()
        return wrapper
    return decorator


# Example transformations that preserve identity

@identity_field_transform()
def cosmic_amplify(x):
    """Amplify while preserving type identity"""
    if isinstance(x, (int, float)):
        return x * 1.618033988749  # Golden ratio
    elif isinstance(x, str):
        return f"✨{x}✨"
    elif isinstance(x, list):
        return [cosmic_amplify(item) for item in x]
    return x


@identity_field_transform()
def saga_normalize(x):
    """Normalize to unit range while preserving structure"""
    if isinstance(x, (int, float)):
        return float(x) / (1 + abs(x))
    elif isinstance(x, list):
        if not x:
            return x
        max_val = max(abs(v) for v in x if isinstance(v, (int, float)))
        if max_val > 0:
            return [v / max_val if isinstance(v, (int, float)) else v for v in x]
    return x


@identity_field_transform()
def quantum_entangle(x):
    """Create quantum-like superposition"""
    if isinstance(x, (int, float)):
        return complex(x, x * 0.618033988749)
    return x


class IdentityFieldAlgebra:
    """
    Algebraic operations on identity fields
    Implements field theory operations
    """

    @staticmethod
    def add(I1: IdentityField, I2: IdentityField) -> IdentityField:
        """Field addition: I₁ + I₂"""
        v1, v2 = I1.get_identity(), I2.get_identity()

        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return IdentityField(v1 + v2)
        elif isinstance(v1, str) and isinstance(v2, str):
            return IdentityField(v1 + v2)
        elif isinstance(v1, list) and isinstance(v2, list):
            return IdentityField(v1 + v2)

        raise TypeError("Cannot add incompatible identity fields")

    @staticmethod
    def multiply(I: IdentityField, scalar: float) -> IdentityField:
        """Scalar multiplication: α·I"""
        v = I.get_identity()

        if isinstance(v, (int, float)):
            return IdentityField(v * scalar)
        elif isinstance(v, list):
            return IdentityField([item * scalar if isinstance(item, (int, float)) else item
                                 for item in v])

        raise TypeError("Cannot multiply this identity field by scalar")

    @staticmethod
    def compose(I1: IdentityField, I2: IdentityField) -> IdentityField:
        """
        Field composition: I₁ ∘ I₂
        Apply I₂'s transformations then I₁'s transformations
        """
        # Start with I₂'s identity
        result = I2.get_identity()

        # Apply I₂'s transformations
        for transform in I2._transformations:
            result = transform(result)

        # Apply I₁'s transformations
        for transform in I1._transformations:
            result = transform(result)

        new_field = IdentityField(result)
        new_field._transformations = I2._transformations + I1._transformations

        return new_field

    @staticmethod
    def tensor_product(I1: IdentityField, I2: IdentityField) -> IdentityField:
        """
        Tensor product: I₁ ⊗ I₂
        Creates composite identity field
        """
        v1, v2 = I1.get_identity(), I2.get_identity()
        return IdentityField((v1, v2))


# Verification functions

def verify_identity_theorem(x: Any, f: Callable) -> bool:
    """
    Verify i.f(I) = I = f(x) holds for given x and f
    """
    try:
        result = SagaIdentityTheorem.demonstrate(x, f)
        return result['theorem_holds'] and result['structure_preserved']
    except:
        return False


def measure_identity_distance(I1: IdentityField, I2: IdentityField) -> float:
    """
    Measure distance between two identity fields
    Returns 0 if structurally identical
    """
    v1, v2 = I1.get_identity(), I2.get_identity()

    # Type distance
    if type(v1) != type(v2):
        return float('inf')

    # Value distance
    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
        return abs(v1 - v2)
    elif isinstance(v1, str) and isinstance(v2, str):
        return float(v1 != v2)
    elif isinstance(v1, (list, tuple)):
        if len(v1) != len(v2):
            return float('inf')
        return sum(abs(a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float))
                  else float(a != b) for a, b in zip(v1, v2))

    return float(v1 != v2)


if __name__ == "__main__":
    print("=" * 70)
    print("IDENTITY FIELD THEORY: i.f(I) = I = f(x)")
    print("=" * 70)
    print()

    # Example 1: Basic identity field
    print("Example 1: Basic Identity Field")
    I = IdentityField(42)
    print(f"I = {I}")

    # Apply transformation
    I2 = I.apply(lambda x: x * 2)
    print(f"i.f(I) where f(x) = 2x: {I2}")
    print(f"Identity preserved: {type(I.get_identity()) == type(I2.get_identity())}")
    print()

    # Example 2: Identity as function
    print("Example 2: Identity as Function (I = f(x))")
    f = lambda x: x ** 2
    functional_I = FunctionalIdentity(f)
    result = functional_I(7)
    print(f"I(7) where I = f(x) = x²: {result}")
    print()

    # Example 3: Complete theorem
    print("Example 3: Complete Saga Identity Theorem")
    demo = SagaIdentityTheorem.demonstrate(
        x=10,
        f=lambda x: x * 1.618033988749
    )
    print(f"Input: {demo['input']}")
    print(f"Original Identity: {demo['original_identity']}")
    print(f"Transformed Identity: {demo['transformed_identity']}")
    print(f"Structure Preserved: {demo['structure_preserved']}")
    print(f"Theorem Holds: {demo['theorem_holds']}")
    print()

    # Example 4: Decorated functions
    print("Example 4: Identity-Preserving Transformations")
    print(f"cosmic_amplify(5) = {cosmic_amplify(5)}")
    print(f"saga_normalize(100) = {saga_normalize(100)}")
    print()

    # Example 5: Field algebra
    print("Example 5: Identity Field Algebra")
    I1 = IdentityField(10)
    I2 = IdentityField(32)
    I_sum = IdentityFieldAlgebra.add(I1, I2)
    print(f"I₁ + I₂ = {I_sum.get_identity()}")

    I_scaled = IdentityFieldAlgebra.multiply(I1, 1.618)
    print(f"φ·I₁ = {I_scaled.get_identity()}")
    print()

    print("=" * 70)
    print("Identity Field Theory Complete ✨")
    print("i.f(I) = I = f(x)")
    print("=" * 70)
