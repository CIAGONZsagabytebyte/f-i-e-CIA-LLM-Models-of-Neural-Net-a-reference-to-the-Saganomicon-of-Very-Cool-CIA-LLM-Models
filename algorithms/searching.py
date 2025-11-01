"""
Searching Algorithms

Classic search algorithm implementations with complexity analysis.
"""

from typing import List, Any, Optional, Callable
from collections import deque


def linear_search(arr: List[Any], target: Any) -> int:
    """
    Linear Search - sequentially checks each element until target is found.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Returns:
        Index of target if found, -1 otherwise
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1


def binary_search(arr: List[Any], target: Any) -> int:
    """
    Binary Search - searches a sorted array by repeatedly dividing
    the search interval in half.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        arr: Sorted array to search
        target: Element to find

    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_recursive(arr: List[Any], target: Any, left: int = 0, right: Optional[int] = None) -> int:
    """
    Binary Search - recursive implementation.

    Time Complexity: O(log n)
    Space Complexity: O(log n) due to recursion stack

    Returns:
        Index of target if found, -1 otherwise
    """
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr: List[Any], target: Any) -> int:
    """
    Find the leftmost (first) occurrence of target in a sorted array.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of leftmost occurrence, -1 if not found
    """
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def binary_search_rightmost(arr: List[Any], target: Any) -> int:
    """
    Find the rightmost (last) occurrence of target in a sorted array.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of rightmost occurrence, -1 if not found
    """
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def jump_search(arr: List[Any], target: Any) -> int:
    """
    Jump Search - searches a sorted array by jumping ahead by fixed steps
    and then performing linear search.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    Returns:
        Index of target if found, -1 otherwise
    """
    import math

    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0

    # Jump to the block where target may exist
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))

        if prev >= n:
            return -1

    # Linear search in the identified block
    while prev < n and arr[prev] < target:
        prev += 1

        if prev == min(step, n):
            return -1

    if prev < n and arr[prev] == target:
        return prev

    return -1


def interpolation_search(arr: List[int], target: int) -> int:
    """
    Interpolation Search - improved binary search for uniformly distributed data.
    Uses value-based position estimation instead of mid-point.

    Time Complexity: O(log log n) for uniform data, O(n) worst case
    Space Complexity: O(1)

    Note: Works best with uniformly distributed sorted arrays of numbers.

    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1

    while left <= right and target >= arr[left] and target <= arr[right]:
        # Avoid division by zero
        if arr[right] == arr[left]:
            if arr[left] == target:
                return left
            return -1

        # Estimate position using interpolation formula
        pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1


def exponential_search(arr: List[Any], target: Any) -> int:
    """
    Exponential Search - finds range where element may exist by repeated doubling,
    then performs binary search.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Useful for unbounded/infinite arrays.

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    if arr[0] == target:
        return 0

    # Find range for binary search
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2

    # Binary search in the identified range
    return binary_search_recursive(arr, target, i // 2, min(i, len(arr) - 1))


def ternary_search(arr: List[Any], target: Any) -> int:
    """
    Ternary Search - divides array into three parts instead of two.

    Time Complexity: O(log₃ n)
    Space Complexity: O(1)

    Note: Generally slower than binary search due to more comparisons,
    but included for educational purposes.

    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1


def find_peak_element(arr: List[Any]) -> int:
    """
    Find a peak element in an array.
    A peak element is greater than its neighbors.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of a peak element
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left


def find_rotation_point(arr: List[Any]) -> int:
    """
    Find the rotation point in a rotated sorted array.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of the minimum element (rotation point)
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > arr[right]:
            left = mid + 1
        else:
            right = mid

    return left


def search_in_rotated_array(arr: List[Any], target: Any) -> int:
    """
    Search for a target in a rotated sorted array.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of target if found, -1 otherwise
    """
    if not arr:
        return -1

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
