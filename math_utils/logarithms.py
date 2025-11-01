"""
Logarithm and Exponential Functions

Mathematical utilities for logarithmic and exponential calculations.
"""

import math
from typing import Union


def natural_log(x: Union[int, float]) -> float:
    """
    Compute the natural logarithm (base e) of x.

    Args:
        x: Positive number

    Returns:
        ln(x)

    Raises:
        ValueError: If x <= 0
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values")

    return math.log(x)


def log_base(x: Union[int, float], base: Union[int, float]) -> float:
    """
    Compute logarithm of x with arbitrary base.

    Args:
        x: Positive number
        base: Positive base (not equal to 1)

    Returns:
        log_base(x)

    Raises:
        ValueError: If x <= 0 or base <= 0 or base == 1
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values")
    if base <= 0 or base == 1:
        raise ValueError("Base must be positive and not equal to 1")

    return math.log(x, base)


def log2(x: Union[int, float]) -> float:
    """
    Compute the binary logarithm (base 2) of x.

    Args:
        x: Positive number

    Returns:
        log₂(x)
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values")

    return math.log2(x)


def log10(x: Union[int, float]) -> float:
    """
    Compute the common logarithm (base 10) of x.

    Args:
        x: Positive number

    Returns:
        log₁₀(x)
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values")

    return math.log10(x)


def ln_taylor_series(x: Union[int, float], terms: int = 100) -> float:
    """
    Compute natural logarithm using Taylor series expansion.

    ln(1 + x) = x - x²/2 + x³/3 - x⁴/4 + ...

    Valid for -1 < x <= 1

    Args:
        x: Number in range (-1, 1]
        terms: Number of terms in the series

    Returns:
        Approximation of ln(1 + x)
    """
    if x <= -1 or x > 1:
        raise ValueError("Taylor series for ln(1+x) requires -1 < x <= 1")

    result = 0
    for n in range(1, terms + 1):
        result += ((-1) ** (n + 1)) * (x ** n) / n

    return result


def exp(x: Union[int, float]) -> float:
    """
    Compute e raised to the power x.

    Args:
        x: Exponent

    Returns:
        e^x
    """
    return math.exp(x)


def exp_taylor_series(x: Union[int, float], terms: int = 50) -> float:
    """
    Compute exponential function using Taylor series.

    e^x = 1 + x + x²/2! + x³/3! + ...

    Args:
        x: Exponent
        terms: Number of terms in the series

    Returns:
        Approximation of e^x
    """
    result = 0
    factorial = 1

    for n in range(terms):
        if n > 0:
            factorial *= n
        result += (x ** n) / factorial

    return result


def power(base: Union[int, float], exponent: Union[int, float]) -> float:
    """
    Compute base raised to the power of exponent.

    Args:
        base: Base number
        exponent: Power to raise to

    Returns:
        base^exponent
    """
    return base ** exponent


def log_product(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Use logarithm properties: ln(a * b) = ln(a) + ln(b)

    Args:
        a, b: Positive numbers

    Returns:
        ln(a * b)
    """
    return natural_log(a) + natural_log(b)


def log_quotient(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Use logarithm properties: ln(a / b) = ln(a) - ln(b)

    Args:
        a, b: Positive numbers

    Returns:
        ln(a / b)
    """
    return natural_log(a) - natural_log(b)


def log_power_property(base: Union[int, float], exponent: Union[int, float]) -> float:
    """
    Use logarithm properties: ln(a^b) = b * ln(a)

    Args:
        base: Positive base
        exponent: Exponent

    Returns:
        ln(base^exponent)
    """
    return exponent * natural_log(base)


def change_of_base(x: Union[int, float], from_base: Union[int, float], to_base: Union[int, float]) -> float:
    """
    Convert logarithm from one base to another.

    log_b(x) = log_c(x) / log_c(b)

    Args:
        x: Value
        from_base: Original base
        to_base: Target base

    Returns:
        Logarithm of x in the new base
    """
    return log_base(x, to_base) / log_base(from_base, to_base)


# Constants
E = math.e
LN_2 = math.log(2)
LN_10 = math.log(10)
LOG2_E = math.log2(math.e)
LOG10_E = math.log10(math.e)
