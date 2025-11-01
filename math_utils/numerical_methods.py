"""
Numerical Methods

Numerical analysis and computational mathematics utilities.
"""

import math
from typing import Callable, Tuple, List, Union


def derivative(f: Callable[[float], float], x: float, h: float = 1e-7) -> float:
    """
    Approximate the derivative of a function at a point using central difference.

    f'(x) ≈ (f(x+h) - f(x-h)) / (2h)

    Args:
        f: Function to differentiate
        x: Point at which to evaluate derivative
        h: Step size (smaller = more accurate but prone to numerical errors)

    Returns:
        Approximate derivative
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def gradient(f: Callable[[List[float]], float], x: List[float], h: float = 1e-7) -> List[float]:
    """
    Compute the gradient of a multivariate function.

    Args:
        f: Multivariate function
        x: Point at which to evaluate gradient
        h: Step size

    Returns:
        Gradient vector
    """
    grad = []

    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()

        x_plus[i] += h
        x_minus[i] -= h

        partial = (f(x_plus) - f(x_minus)) / (2 * h)
        grad.append(partial)

    return grad


def newton_raphson(f: Callable[[float], float],
                   df: Callable[[float], float],
                   x0: float,
                   tolerance: float = 1e-10,
                   max_iterations: int = 100) -> Tuple[float, int]:
    """
    Find root of a function using Newton-Raphson method.

    x_{n+1} = x_n - f(x_n) / f'(x_n)

    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations

    Returns:
        Tuple of (root, iterations)

    Raises:
        RuntimeError: If method doesn't converge
    """
    x = x0

    for i in range(max_iterations):
        fx = f(x)

        if abs(fx) < tolerance:
            return x, i

        dfx = df(x)

        if abs(dfx) < 1e-15:
            raise RuntimeError("Derivative too close to zero")

        x = x - fx / dfx

    raise RuntimeError(f"Newton-Raphson did not converge within {max_iterations} iterations")


def bisection(f: Callable[[float], float],
              a: float,
              b: float,
              tolerance: float = 1e-10,
              max_iterations: int = 100) -> Tuple[float, int]:
    """
    Find root of a function using bisection method.

    Requires f(a) and f(b) to have opposite signs.

    Args:
        f: Function to find root of
        a, b: Interval endpoints
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations

    Returns:
        Tuple of (root, iterations)

    Raises:
        ValueError: If f(a) and f(b) have the same sign
        RuntimeError: If method doesn't converge
    """
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    for i in range(max_iterations):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tolerance or (b - a) / 2 < tolerance:
            return c, i

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    raise RuntimeError(f"Bisection did not converge within {max_iterations} iterations")


def trapezoidal_rule(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """
    Approximate definite integral using trapezoidal rule.

    ∫[a,b] f(x)dx ≈ h/2 * (f(x_0) + 2*f(x_1) + ... + 2*f(x_{n-1}) + f(x_n))

    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of trapezoids

    Returns:
        Approximate integral
    """
    h = (b - a) / n
    result = (f(a) + f(b)) / 2

    for i in range(1, n):
        x = a + i * h
        result += f(x)

    return result * h


def simpsons_rule(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """
    Approximate definite integral using Simpson's rule.

    More accurate than trapezoidal rule.

    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals (must be even)

    Returns:
        Approximate integral

    Raises:
        ValueError: If n is not even
    """
    if n % 2 != 0:
        raise ValueError("n must be even for Simpson's rule")

    h = (b - a) / n
    result = f(a) + f(b)

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            result += 2 * f(x)
        else:
            result += 4 * f(x)

    return result * h / 3


def euler_method(f: Callable[[float, float], float],
                 y0: float,
                 t0: float,
                 t_end: float,
                 h: float) -> List[Tuple[float, float]]:
    """
    Solve ODE using Euler's method.

    dy/dt = f(t, y), y(t0) = y0

    Args:
        f: Function defining the ODE
        y0: Initial condition
        t0: Initial time
        t_end: End time
        h: Step size

    Returns:
        List of (t, y) tuples
    """
    results = [(t0, y0)]
    t = t0
    y = y0

    while t < t_end:
        y = y + h * f(t, y)
        t = t + h
        results.append((t, y))

    return results


def runge_kutta_4(f: Callable[[float, float], float],
                  y0: float,
                  t0: float,
                  t_end: float,
                  h: float) -> List[Tuple[float, float]]:
    """
    Solve ODE using 4th-order Runge-Kutta method.

    More accurate than Euler's method.

    dy/dt = f(t, y), y(t0) = y0

    Args:
        f: Function defining the ODE
        y0: Initial condition
        t0: Initial time
        t_end: End time
        h: Step size

    Returns:
        List of (t, y) tuples
    """
    results = [(t0, y0)]
    t = t0
    y = y0

    while t < t_end:
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)

        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        t = t + h
        results.append((t, y))

    return results


def fibonacci_sequence(n: int) -> List[int]:
    """
    Generate the first n Fibonacci numbers.

    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)

    Args:
        n: Number of Fibonacci numbers to generate

    Returns:
        List of Fibonacci numbers
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]

    fib = [0, 1]

    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])

    return fib


def golden_ratio_approximation(n: int = 20) -> float:
    """
    Approximate the golden ratio using Fibonacci sequence.

    φ ≈ F(n) / F(n-1) as n → ∞

    Args:
        n: Number of iterations

    Returns:
        Approximation of golden ratio
    """
    fib = fibonacci_sequence(n + 1)
    return fib[n] / fib[n-1]


def factorial(n: int) -> int:
    """
    Calculate factorial of n.

    n! = n × (n-1) × ... × 2 × 1

    Args:
        n: Non-negative integer

    Returns:
        n!

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")

    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


def binomial_coefficient(n: int, k: int) -> int:
    """
    Calculate binomial coefficient C(n, k) = n! / (k! * (n-k)!)

    Args:
        n: Total items
        k: Items to choose

    Returns:
        Binomial coefficient

    Raises:
        ValueError: If k > n or k < 0
    """
    if k > n or k < 0:
        raise ValueError("Invalid values for binomial coefficient")

    if k == 0 or k == n:
        return 1

    # Optimize by using smaller k
    k = min(k, n - k)

    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)

    return result


def gcd(a: int, b: int) -> int:
    """
    Calculate greatest common divisor using Euclidean algorithm.

    Args:
        a, b: Integers

    Returns:
        GCD of a and b
    """
    a, b = abs(a), abs(b)

    while b:
        a, b = b, a % b

    return a


def lcm(a: int, b: int) -> int:
    """
    Calculate least common multiple.

    LCM(a, b) = |a * b| / GCD(a, b)

    Args:
        a, b: Integers

    Returns:
        LCM of a and b
    """
    if a == 0 or b == 0:
        return 0

    return abs(a * b) // gcd(a, b)


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if prime, False otherwise
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True


def prime_factors(n: int) -> List[int]:
    """
    Find all prime factors of n.

    Args:
        n: Integer to factorize

    Returns:
        List of prime factors
    """
    if n < 2:
        return []

    factors = []

    # Check for factor of 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    if n > 2:
        factors.append(n)

    return factors
