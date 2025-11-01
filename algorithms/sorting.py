"""
Sorting Algorithms

Classic sorting algorithm implementations with time and space complexity analysis.
"""

from typing import List, Any, Callable
import random


def bubble_sort(arr: List[Any]) -> List[Any]:
    """
    Bubble Sort - repeatedly steps through the list, compares adjacent elements
    and swaps them if they are in the wrong order.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    Stable: Yes
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # Optimization: if no swaps occurred, array is sorted
        if not swapped:
            break

    return arr


def selection_sort(arr: List[Any]) -> List[Any]:
    """
    Selection Sort - divides the array into sorted and unsorted regions,
    repeatedly selecting the minimum element from unsorted region.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    Stable: No
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def insertion_sort(arr: List[Any]) -> List[Any]:
    """
    Insertion Sort - builds the sorted array one item at a time,
    inserting each element into its correct position.

    Time Complexity: O(n²) worst case, O(n) best case
    Space Complexity: O(1)
    Stable: Yes
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def merge_sort(arr: List[Any]) -> List[Any]:
    """
    Merge Sort - divide-and-conquer algorithm that divides the array
    into halves, sorts them, and merges them back together.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    Stable: Yes
    """
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left: List[Any], right: List[Any]) -> List[Any]:
    """Helper function to merge two sorted arrays."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def quick_sort(arr: List[Any]) -> List[Any]:
    """
    Quick Sort - divide-and-conquer algorithm that selects a pivot element
    and partitions the array around it.

    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) average
    Stable: No
    """
    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr: List[Any], low: int, high: int) -> None:
    """Helper function for quick sort."""
    if low < high:
        pivot_idx = _partition(arr, low, high)
        _quick_sort_helper(arr, low, pivot_idx - 1)
        _quick_sort_helper(arr, pivot_idx + 1, high)


def _partition(arr: List[Any], low: int, high: int) -> int:
    """Partition array around pivot element."""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def heap_sort(arr: List[Any]) -> List[Any]:
    """
    Heap Sort - builds a max heap and repeatedly extracts the maximum element.

    Time Complexity: O(n log n)
    Space Complexity: O(1)
    Stable: No
    """
    arr = arr.copy()
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)

    return arr


def _heapify(arr: List[Any], n: int, i: int) -> None:
    """Heapify subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def counting_sort(arr: List[int]) -> List[int]:
    """
    Counting Sort - integer sorting algorithm that counts occurrences
    of each value. Works well for small range of integers.

    Time Complexity: O(n + k) where k is the range
    Space Complexity: O(k)
    Stable: Yes

    Note: Only works with non-negative integers.
    """
    if not arr:
        return []

    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1

    count = [0] * range_size
    output = [0] * len(arr)

    # Count occurrences
    for num in arr:
        count[num - min_val] += 1

    # Calculate cumulative count
    for i in range(1, range_size):
        count[i] += count[i - 1]

    # Build output array
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output


def radix_sort(arr: List[int]) -> List[int]:
    """
    Radix Sort - sorts integers by processing individual digits.

    Time Complexity: O(d * (n + k)) where d is number of digits
    Space Complexity: O(n + k)
    Stable: Yes

    Note: Only works with non-negative integers.
    """
    if not arr:
        return []

    max_val = max(arr)
    exp = 1

    arr = arr.copy()

    while max_val // exp > 0:
        _counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr


def _counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """Helper function for radix sort - sorts by digit at position exp."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    for i in range(n):
        arr[i] = output[i]


def is_sorted(arr: List[Any], reverse: bool = False) -> bool:
    """
    Check if an array is sorted.

    Args:
        arr: The array to check
        reverse: If True, check for descending order

    Returns:
        True if sorted, False otherwise
    """
    if len(arr) <= 1:
        return True

    if reverse:
        return all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1))
    else:
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
