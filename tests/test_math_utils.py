"""
Unit tests for mathematical utilities.
"""

import sys
sys.path.insert(0, '..')

import math
from math_utils.logarithms import *
from math_utils.statistics import *
from math_utils.numerical_methods import *


def test_logarithms():
    """Test logarithm functions."""
    # Test natural log
    assert abs(natural_log(math.e) - 1.0) < 1e-10
    assert abs(natural_log(1) - 0.0) < 1e-10

    # Test log base
    assert abs(log_base(100, 10) - 2.0) < 1e-10
    assert abs(log_base(8, 2) - 3.0) < 1e-10

    # Test exponential
    assert abs(exp(0) - 1.0) < 1e-10
    assert abs(exp(1) - math.e) < 1e-10

    # Test logarithm properties
    assert abs(log_product(2, 3) - natural_log(6)) < 1e-10
    assert abs(log_quotient(6, 2) - natural_log(3)) < 1e-10

    print("✓ Logarithm tests passed")


def test_statistics():
    """Test statistical functions."""
    data = [2, 4, 4, 4, 5, 5, 7, 9]

    # Test mean
    assert mean(data) == 5.0

    # Test median
    assert median(data) == 4.5

    # Test mode
    assert mode(data) == [4]

    # Test variance
    var = variance(data, sample=False)
    assert abs(var - 4.0) < 1e-10

    # Test standard deviation
    std = standard_deviation(data, sample=False)
    assert abs(std - 2.0) < 1e-10

    # Test percentile
    assert percentile(data, 50) == 4.5  # Median
    assert percentile(data, 0) == 2
    assert percentile(data, 100) == 9

    # Test range
    assert range_stat(data) == 7

    # Test correlation
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    corr = correlation(x, y)
    assert abs(corr - 1.0) < 1e-10  # Perfect positive correlation

    print("✓ Statistics tests passed")


def test_numerical_methods():
    """Test numerical methods."""
    # Test derivative
    f = lambda x: x**2
    deriv = derivative(f, 3)
    assert abs(deriv - 6.0) < 1e-5  # f'(x) = 2x, f'(3) = 6

    # Test Newton-Raphson (find square root of 2)
    f = lambda x: x**2 - 2
    df = lambda x: 2*x
    root, _ = newton_raphson(f, df, 1.0)
    assert abs(root - math.sqrt(2)) < 1e-10

    # Test bisection (find root of f(x) = x^2 - 4)
    f = lambda x: x**2 - 4
    root, _ = bisection(f, 0, 3)
    assert abs(root - 2.0) < 1e-10

    # Test integration (∫₀¹ x² dx = 1/3)
    f = lambda x: x**2
    result = simpsons_rule(f, 0, 1, n=100)
    assert abs(result - 1/3) < 1e-5

    # Test Fibonacci
    fib = fibonacci_sequence(10)
    assert fib == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # Test factorial
    assert factorial(5) == 120
    assert factorial(0) == 1

    # Test GCD
    assert gcd(48, 18) == 6
    assert gcd(17, 19) == 1

    # Test LCM
    assert lcm(4, 6) == 12
    assert lcm(7, 5) == 35

    # Test prime checking
    assert is_prime(17) == True
    assert is_prime(18) == False
    assert is_prime(2) == True

    # Test prime factors
    assert prime_factors(60) == [2, 2, 3, 5]
    assert prime_factors(17) == [17]

    print("✓ Numerical methods tests passed")


if __name__ == "__main__":
    test_logarithms()
    test_statistics()
    test_numerical_methods()
    print("\n✓ All math utility tests passed!")
