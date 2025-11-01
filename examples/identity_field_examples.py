"""
Identity Field Examples - Demonstrating i.f(I) = I = f(x)

The foundational principle where:
- i: identity operator
- f: transformation function
- I: Identity field (preserved through transformation)
- x: input value

By PAUL RUTHERFORDS
"""

from io_fields import (
    IdentityField,
    IdentityOperator,
    FunctionalIdentity,
    SagaIdentityTheorem,
    IdentityFieldAlgebra,
    identity_field_transform
)


def example_1_basic_identity():
    """Example 1: Basic Identity Field Creation and Transformation"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Identity Field")
    print("=" * 70)

    # Create identity field from value
    I = IdentityField(42)
    print(f"I = IdentityField(42)")
    print(f"  {I}")
    print()

    # Apply transformation: i.f(I) = I
    print("Applying f(x) = 2x:")
    I_doubled = I.apply(lambda x: x * 2)
    print(f"  i.f(I) = {I_doubled}")
    print(f"  Value: {I_doubled.get_identity()}")
    print(f"  Type preserved: {type(I.get_identity()) == type(I_doubled.get_identity())}")
    print()

    # Chain transformations
    print("Chaining transformations:")
    I_chained = I.apply(lambda x: x * 2).apply(lambda x: x + 10).apply(lambda x: x / 2)
    print(f"  ((42 * 2) + 10) / 2 = {I_chained.get_identity()}")
    print(f"  Lineage: {I_chained.get_lineage()}")
    print()


def example_2_identity_as_function():
    """Example 2: Identity IS a Function (I = f(x))"""
    print("=" * 70)
    print("EXAMPLE 2: Identity as Function")
    print("=" * 70)

    # Define function
    def quadratic(x):
        return x ** 2 + 2 * x + 1

    # Create functional identity
    I = FunctionalIdentity(quadratic)
    print(f"I = FunctionalIdentity(x² + 2x + 1)")
    print()

    # Use identity as function
    for x in [0, 1, 2, 5, 10]:
        result = I(x)
        print(f"  I({x}) = {result}")
    print()

    # Compose with another function
    print("Composing I with g(x) = x + 1:")
    I_composed = I.compose(lambda x: x + 1)
    print(f"  (I ∘ g)(5) = I(g(5)) = I(6) = {I_composed(5)}")
    print()


def example_3_complete_theorem():
    """Example 3: Complete Saga Identity Theorem"""
    print("=" * 70)
    print("EXAMPLE 3: Complete Saga Identity Theorem - i.f(I) = I = f(x)")
    print("=" * 70)

    # Golden ratio transformation
    phi = 1.618033988749

    demo = SagaIdentityTheorem.demonstrate(
        x=100,
        f=lambda x: x * phi
    )

    print(f"Input value (x): {demo['input']}")
    print(f"Function: f(x) = φ·x where φ = {phi}")
    print()

    print("Left side - i.f(I) = I:")
    print(f"  Original Identity: {demo['original_identity']}")
    print(f"  After transformation: {demo['transformed_identity']}")
    print(f"  Structure preserved: {demo['structure_preserved']}")
    print()

    print("Right side - I = f(x):")
    print(f"  Functional result: {demo['functional_result']}")
    print()

    print(f"Theorem holds: {demo['theorem_holds']} ✨")
    print()


def example_4_decorated_functions():
    """Example 4: Identity-Preserving Decorators"""
    print("=" * 70)
    print("EXAMPLE 4: Identity-Preserving Transformations")
    print("=" * 70)

    @identity_field_transform()
    def fibonacci_transform(x):
        """Transform to nearest Fibonacci number"""
        if not isinstance(x, (int, float)):
            return x

        n = int(abs(x))
        a, b = 0, 1
        while b < n:
            a, b = b, a + b

        # Return closest
        return a if abs(n - a) < abs(n - b) else b

    @identity_field_transform()
    def cosmic_wave(x):
        """Apply cosmic wave transformation"""
        import math
        if isinstance(x, (int, float)):
            return x * math.sin(x / 10) + x
        return x

    print("Decorated functions preserve identity structure:")
    print()

    # Test with regular values
    print("fibonacci_transform(100) =", fibonacci_transform(100))
    print("fibonacci_transform(50) =", fibonacci_transform(50))
    print()

    # Test with identity fields
    I = IdentityField(42)
    I_fib = fibonacci_transform(I)
    print(f"fibonacci_transform(IdentityField(42)) = {I_fib}")
    print()

    # Chain transformations
    result = cosmic_wave(fibonacci_transform(100))
    print(f"cosmic_wave(fibonacci_transform(100)) = {result}")
    print()


def example_5_field_algebra():
    """Example 5: Identity Field Algebra"""
    print("=" * 70)
    print("EXAMPLE 5: Identity Field Algebra")
    print("=" * 70)

    # Create identity fields
    I1 = IdentityField(10)
    I2 = IdentityField(32)
    print(f"I₁ = {I1.get_identity()}")
    print(f"I₂ = {I2.get_identity()}")
    print()

    # Addition
    print("Field Addition:")
    I_sum = IdentityFieldAlgebra.add(I1, I2)
    print(f"  I₁ + I₂ = {I_sum.get_identity()}")
    print()

    # Scalar multiplication
    print("Scalar Multiplication:")
    phi = 1.618033988749
    I_scaled = IdentityFieldAlgebra.multiply(I1, phi)
    print(f"  φ·I₁ = {I_scaled.get_identity()}")
    print()

    # Composition
    print("Field Composition:")
    I1_transformed = I1.apply(lambda x: x * 2)
    I2_transformed = I2.apply(lambda x: x + 5)
    I_composed = IdentityFieldAlgebra.compose(I1_transformed, I2_transformed)
    print(f"  I₁ ∘ I₂ = {I_composed.get_identity()}")
    print()

    # Tensor product
    print("Tensor Product:")
    I_tensor = IdentityFieldAlgebra.tensor_product(I1, I2)
    print(f"  I₁ ⊗ I₂ = {I_tensor.get_identity()}")
    print()


def example_6_transformation_chains():
    """Example 6: Complex Transformation Chains"""
    print("=" * 70)
    print("EXAMPLE 6: Complex Transformation Chains")
    print("=" * 70)

    # Create transformation chain
    chain = SagaIdentityTheorem.compose_chain(
        lambda x: x * 2,      # f₁: double
        lambda x: x + 10,     # f₂: add 10
        lambda x: x ** 2,     # f₃: square
        lambda x: x / 100     # f₄: normalize
    )

    print("Transformation chain: f₄ ∘ f₃ ∘ f₂ ∘ f₁")
    print("  f₁(x) = 2x")
    print("  f₂(x) = x + 10")
    print("  f₃(x) = x²")
    print("  f₄(x) = x / 100")
    print()

    for x in [5, 10, 20]:
        result = chain(x)
        print(f"  Chain({x}) = {result}")
    print()


def example_7_identity_verification():
    """Example 7: Verifying Identity Preservation"""
    print("=" * 70)
    print("EXAMPLE 7: Identity Verification")
    print("=" * 70)

    from io_fields.identity_field import verify_identity_theorem, measure_identity_distance

    # Test various transformations
    transformations = [
        ("f(x) = 2x", lambda x: x * 2),
        ("f(x) = x + 100", lambda x: x + 100),
        ("f(x) = x²", lambda x: x ** 2),
        ("f(x) = √x", lambda x: x ** 0.5),
        ("f(x) = φx", lambda x: x * 1.618033988749),
    ]

    test_value = 42
    print(f"Testing with x = {test_value}")
    print()

    for name, func in transformations:
        holds = verify_identity_theorem(test_value, func)
        print(f"  {name}: {'✓ Theorem holds' if holds else '✗ Theorem fails'}")
    print()

    # Measure distances
    print("Identity Field Distances:")
    I1 = IdentityField(10)
    I2 = IdentityField(10.0)
    I3 = IdentityField(20)

    print(f"  distance(I₁=10, I₂=10.0) = {measure_identity_distance(I1, I2)}")
    print(f"  distance(I₁=10, I₃=20) = {measure_identity_distance(I1, I3)}")
    print()


def example_8_list_transformations():
    """Example 8: Identity Fields with Collections"""
    print("=" * 70)
    print("EXAMPLE 8: Identity Fields with Collections")
    print("=" * 70)

    # List identity field
    I_list = IdentityField([1, 2, 3, 4, 5])
    print(f"I = {I_list.get_identity()}")
    print()

    # Transform each element
    print("Transforming each element:")
    I_doubled = I_list.apply(lambda lst: [x * 2 for x in lst])
    print(f"  Double each: {I_doubled.get_identity()}")

    I_squared = I_list.apply(lambda lst: [x ** 2 for x in lst])
    print(f"  Square each: {I_squared.get_identity()}")
    print()

    # Aggregate transformations (break identity structure)
    print("Aggregate transformations (require new identity field):")
    try:
        I_sum = I_list.apply(lambda lst: sum(lst))
        print(f"  Sum: {I_sum.get_identity()}")
    except ValueError as e:
        print(f"  Sum breaks structure: {e}")
        # Create new identity field for aggregated value
        sum_value = sum(I_list.get_identity())
        I_sum_new = IdentityField(sum_value)
        print(f"  New identity for sum: {I_sum_new.get_identity()}")
    print()


def example_9_quantum_identity():
    """Example 9: Quantum Identity Transformations"""
    print("=" * 70)
    print("EXAMPLE 9: Quantum Identity Transformations")
    print("=" * 70)

    # Complex number identity fields
    I = IdentityField(5)
    print(f"Real identity: I = {I.get_identity()}")
    print()

    # Transform to complex
    I_complex = I.apply(lambda x: complex(x, x * 0.618))
    print(f"Quantum entanglement: I = {I_complex.get_identity()}")
    print(f"  Real part: {I_complex.get_identity().real}")
    print(f"  Imaginary part: {I_complex.get_identity().imag}")
    print()

    # Apply quantum rotation
    import cmath
    I_rotated = I_complex.apply(lambda z: z * cmath.exp(1j * cmath.pi / 4))
    print(f"Quantum rotation (π/4): I = {I_rotated.get_identity()}")
    print(f"  Magnitude: {abs(I_rotated.get_identity())}")
    print(f"  Phase: {cmath.phase(I_rotated.get_identity())}")
    print()


def main():
    """Run all identity field examples"""
    print("\n" + "=" * 70)
    print("IDENTITY FIELD THEORY EXAMPLES")
    print("i.f(I) = I = f(x)")
    print("By PAUL RUTHERFORDS")
    print("=" * 70 + "\n")

    try:
        example_1_basic_identity()
        example_2_identity_as_function()
        example_3_complete_theorem()
        example_4_decorated_functions()
        example_5_field_algebra()
        example_6_transformation_chains()
        example_7_identity_verification()
        example_8_list_transformations()
        example_9_quantum_identity()

        print("=" * 70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY ✨")
        print("Identity preserved through cosmic transformations")
        print("i.f(I) = I = f(x)")
        print("=" * 70)

    except Exception as e:
        print(f"\nError in examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
