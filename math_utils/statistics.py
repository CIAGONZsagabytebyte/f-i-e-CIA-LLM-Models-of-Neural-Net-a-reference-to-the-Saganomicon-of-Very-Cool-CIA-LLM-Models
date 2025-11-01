"""
Statistical Functions

Common statistical calculations and measures.
"""

import math
from typing import List, Union, Tuple


def mean(data: List[Union[int, float]]) -> float:
    """
    Calculate the arithmetic mean (average) of a dataset.

    Args:
        data: List of numbers

    Returns:
        Mean value

    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate mean of empty dataset")

    return sum(data) / len(data)


def median(data: List[Union[int, float]]) -> float:
    """
    Calculate the median (middle value) of a dataset.

    Args:
        data: List of numbers

    Returns:
        Median value

    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate median of empty dataset")

    sorted_data = sorted(data)
    n = len(sorted_data)

    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]


def mode(data: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Calculate the mode (most frequent value) of a dataset.

    Args:
        data: List of numbers

    Returns:
        List of mode values (may be multiple)

    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate mode of empty dataset")

    frequency = {}
    for value in data:
        frequency[value] = frequency.get(value, 0) + 1

    max_freq = max(frequency.values())
    return [value for value, freq in frequency.items() if freq == max_freq]


def variance(data: List[Union[int, float]], sample: bool = True) -> float:
    """
    Calculate the variance of a dataset.

    Args:
        data: List of numbers
        sample: If True, use sample variance (n-1). If False, use population variance (n)

    Returns:
        Variance

    Raises:
        ValueError: If data is empty or has only one element when sample=True
    """
    if not data:
        raise ValueError("Cannot calculate variance of empty dataset")

    if sample and len(data) < 2:
        raise ValueError("Sample variance requires at least 2 data points")

    avg = mean(data)
    squared_diffs = [(x - avg) ** 2 for x in data]

    divisor = len(data) - 1 if sample else len(data)
    return sum(squared_diffs) / divisor


def standard_deviation(data: List[Union[int, float]], sample: bool = True) -> float:
    """
    Calculate the standard deviation of a dataset.

    Args:
        data: List of numbers
        sample: If True, use sample std dev. If False, use population std dev

    Returns:
        Standard deviation
    """
    return math.sqrt(variance(data, sample))


def covariance(x: List[Union[int, float]], y: List[Union[int, float]], sample: bool = True) -> float:
    """
    Calculate the covariance between two datasets.

    Args:
        x, y: Lists of numbers (must be same length)
        sample: If True, use sample covariance (n-1). If False, use population covariance (n)

    Returns:
        Covariance

    Raises:
        ValueError: If datasets have different lengths or are too small
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have the same length")

    if not x:
        raise ValueError("Cannot calculate covariance of empty datasets")

    if sample and len(x) < 2:
        raise ValueError("Sample covariance requires at least 2 data points")

    mean_x = mean(x)
    mean_y = mean(y)

    cov_sum = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))

    divisor = len(x) - 1 if sample else len(x)
    return cov_sum / divisor


def correlation(x: List[Union[int, float]], y: List[Union[int, float]]) -> float:
    """
    Calculate the Pearson correlation coefficient between two datasets.

    Args:
        x, y: Lists of numbers (must be same length)

    Returns:
        Correlation coefficient (-1 to 1)

    Raises:
        ValueError: If datasets have different lengths or are too small
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have the same length")

    if len(x) < 2:
        raise ValueError("Correlation requires at least 2 data points")

    cov = covariance(x, y, sample=True)
    std_x = standard_deviation(x, sample=True)
    std_y = standard_deviation(y, sample=True)

    if std_x == 0 or std_y == 0:
        raise ValueError("Cannot calculate correlation when standard deviation is zero")

    return cov / (std_x * std_y)


def percentile(data: List[Union[int, float]], p: float) -> float:
    """
    Calculate the p-th percentile of a dataset.

    Args:
        data: List of numbers
        p: Percentile to calculate (0-100)

    Returns:
        Value at the p-th percentile

    Raises:
        ValueError: If data is empty or p is out of range
    """
    if not data:
        raise ValueError("Cannot calculate percentile of empty dataset")

    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")

    sorted_data = sorted(data)
    index = (p / 100) * (len(sorted_data) - 1)

    if index.is_integer():
        return sorted_data[int(index)]
    else:
        lower = sorted_data[int(math.floor(index))]
        upper = sorted_data[int(math.ceil(index))]
        fraction = index - math.floor(index)
        return lower + fraction * (upper - lower)


def quartiles(data: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Calculate the quartiles (Q1, Q2, Q3) of a dataset.

    Args:
        data: List of numbers

    Returns:
        Tuple of (Q1, Q2, Q3)
    """
    return (percentile(data, 25), percentile(data, 50), percentile(data, 75))


def interquartile_range(data: List[Union[int, float]]) -> float:
    """
    Calculate the interquartile range (IQR) of a dataset.

    IQR = Q3 - Q1

    Args:
        data: List of numbers

    Returns:
        Interquartile range
    """
    q1, q2, q3 = quartiles(data)
    return q3 - q1


def z_score(value: Union[int, float], data: List[Union[int, float]]) -> float:
    """
    Calculate the z-score of a value relative to a dataset.

    z = (x - μ) / σ

    Args:
        value: Value to calculate z-score for
        data: Reference dataset

    Returns:
        Z-score
    """
    avg = mean(data)
    std = standard_deviation(data)

    if std == 0:
        raise ValueError("Cannot calculate z-score when standard deviation is zero")

    return (value - avg) / std


def min_max_normalize(data: List[Union[int, float]]) -> List[float]:
    """
    Normalize data to range [0, 1] using min-max normalization.

    normalized = (x - min) / (max - min)

    Args:
        data: List of numbers

    Returns:
        List of normalized values

    Raises:
        ValueError: If all values are the same
    """
    if not data:
        return []

    min_val = min(data)
    max_val = max(data)

    if min_val == max_val:
        raise ValueError("Cannot normalize data with all identical values")

    return [(x - min_val) / (max_val - min_val) for x in data]


def z_score_normalize(data: List[Union[int, float]]) -> List[float]:
    """
    Normalize data using z-score normalization (standardization).

    normalized = (x - μ) / σ

    Args:
        data: List of numbers

    Returns:
        List of normalized values
    """
    if not data:
        return []

    avg = mean(data)
    std = standard_deviation(data)

    if std == 0:
        raise ValueError("Cannot normalize data with zero standard deviation")

    return [(x - avg) / std for x in data]


def range_stat(data: List[Union[int, float]]) -> float:
    """
    Calculate the range of a dataset.

    range = max - min

    Args:
        data: List of numbers

    Returns:
        Range

    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate range of empty dataset")

    return max(data) - min(data)
