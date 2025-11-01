"""
Heap Implementation

Provides min-heap and max-heap data structures.
"""

from typing import Any, List, Callable, Optional
import heapq


class MinHeap:
    """
    Min Heap implementation.

    A complete binary tree where each parent node is smaller than its children.

    Time Complexity:
        - Insert: O(log n)
        - Extract min: O(log n)
        - Peek min: O(1)
        - Heapify: O(n)
    """

    def __init__(self, items: Optional[List[Any]] = None):
        self.heap: List[Any] = []
        if items:
            self.heap = items.copy()
            heapq.heapify(self.heap)

    def push(self, item: Any) -> None:
        """Insert an item into the heap."""
        heapq.heappush(self.heap, item)

    def pop(self) -> Any:
        """Remove and return the minimum item."""
        if not self.heap:
            raise IndexError("pop from empty heap")
        return heapq.heappop(self.heap)

    def peek(self) -> Any:
        """Return the minimum item without removing it."""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def push_pop(self, item: Any) -> Any:
        """Push item and pop the minimum. More efficient than push() then pop()."""
        return heapq.heappushpop(self.heap, item)

    def replace(self, item: Any) -> Any:
        """Pop minimum and push item. More efficient than pop() then push()."""
        if not self.heap:
            raise IndexError("replace on empty heap")
        return heapq.heapreplace(self.heap, item)

    def nsmallest(self, n: int) -> List[Any]:
        """Return a list of the n smallest items."""
        return heapq.nsmallest(n, self.heap)

    def __len__(self) -> int:
        return len(self.heap)

    def __bool__(self) -> bool:
        return bool(self.heap)

    def __repr__(self) -> str:
        return f"MinHeap({self.heap})"


class MaxHeap:
    """
    Max Heap implementation.

    A complete binary tree where each parent node is larger than its children.
    Implemented using MinHeap with negated values.

    Time Complexity:
        - Insert: O(log n)
        - Extract max: O(log n)
        - Peek max: O(1)
        - Heapify: O(n)
    """

    def __init__(self, items: Optional[List[Any]] = None):
        self.heap: List[Any] = []
        if items:
            # Negate values for max heap behavior
            self.heap = [-x for x in items]
            heapq.heapify(self.heap)

    def push(self, item: Any) -> None:
        """Insert an item into the heap."""
        heapq.heappush(self.heap, -item)

    def pop(self) -> Any:
        """Remove and return the maximum item."""
        if not self.heap:
            raise IndexError("pop from empty heap")
        return -heapq.heappop(self.heap)

    def peek(self) -> Any:
        """Return the maximum item without removing it."""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return -self.heap[0]

    def push_pop(self, item: Any) -> Any:
        """Push item and pop the maximum."""
        return -heapq.heappushpop(self.heap, -item)

    def replace(self, item: Any) -> Any:
        """Pop maximum and push item."""
        if not self.heap:
            raise IndexError("replace on empty heap")
        return -heapq.heapreplace(self.heap, -item)

    def nlargest(self, n: int) -> List[Any]:
        """Return a list of the n largest items."""
        return [-x for x in heapq.nsmallest(n, self.heap)]

    def __len__(self) -> int:
        return len(self.heap)

    def __bool__(self) -> bool:
        return bool(self.heap)

    def __repr__(self) -> str:
        actual_values = [-x for x in self.heap]
        return f"MaxHeap({actual_values})"


class PriorityQueue:
    """
    Priority Queue implementation using min heap.

    Items with lower priority values are dequeued first.
    """

    def __init__(self):
        self.heap: List[tuple] = []
        self.entry_count = 0

    def enqueue(self, item: Any, priority: float = 0) -> None:
        """
        Add an item with a given priority.

        Items with lower priority values are dequeued first.
        """
        # Use entry_count to break ties and maintain FIFO for same priority
        heapq.heappush(self.heap, (priority, self.entry_count, item))
        self.entry_count += 1

    def dequeue(self) -> Any:
        """Remove and return the item with the lowest priority."""
        if not self.heap:
            raise IndexError("dequeue from empty priority queue")
        priority, count, item = heapq.heappop(self.heap)
        return item

    def peek(self) -> Any:
        """Return the item with the lowest priority without removing it."""
        if not self.heap:
            raise IndexError("peek from empty priority queue")
        priority, count, item = self.heap[0]
        return item

    def __len__(self) -> int:
        return len(self.heap)

    def __bool__(self) -> bool:
        return bool(self.heap)

    def __repr__(self) -> str:
        items = [(priority, item) for priority, count, item in self.heap]
        return f"PriorityQueue({items})"
