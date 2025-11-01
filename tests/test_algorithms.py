"""
Unit tests for algorithms.
"""

import sys
sys.path.insert(0, '..')

from algorithms.sorting import *
from algorithms.searching import *


def test_sorting_algorithms():
    """Test all sorting algorithms."""
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    expected = [11, 12, 22, 25, 34, 64, 90]

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Heap Sort", heap_sort),
    ]

    for name, algo in algorithms:
        result = algo(unsorted)
        assert result == expected, f"{name} failed"
        assert is_sorted(result), f"{name} result not sorted"

    # Test counting sort (integers only)
    assert counting_sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]

    # Test radix sort (non-negative integers only)
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]

    print("✓ Sorting algorithm tests passed")


def test_searching_algorithms():
    """Test all searching algorithms."""
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    # Test linear search
    assert linear_search(sorted_array, 7) == 3
    assert linear_search(sorted_array, 20) == -1

    # Test binary search
    assert binary_search(sorted_array, 7) == 3
    assert binary_search(sorted_array, 20) == -1

    # Test recursive binary search
    assert binary_search_recursive(sorted_array, 9) == 4
    assert binary_search_recursive(sorted_array, 100) == -1

    # Test jump search
    assert jump_search(sorted_array, 13) == 6
    assert jump_search(sorted_array, 2) == -1

    # Test exponential search
    assert exponential_search(sorted_array, 11) == 5
    assert exponential_search(sorted_array, 0) == -1

    # Test search in rotated array
    rotated = [7, 9, 11, 13, 15, 1, 3, 5]
    assert search_in_rotated_array(rotated, 13) == 3
    assert search_in_rotated_array(rotated, 3) == 6

    # Test find peak element
    assert find_peak_element([1, 2, 3, 1]) in [2]
    assert find_peak_element([1, 2, 1, 3, 5, 6, 4]) in [1, 5]

    print("✓ Searching algorithm tests passed")


if __name__ == "__main__":
    test_sorting_algorithms()
    test_searching_algorithms()
    print("\n✓ All algorithm tests passed!")
