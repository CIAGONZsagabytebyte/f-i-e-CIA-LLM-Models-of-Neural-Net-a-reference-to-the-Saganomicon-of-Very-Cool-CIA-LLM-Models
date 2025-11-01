"""
Unit tests for data structures.
"""

import sys
sys.path.insert(0, '..')

from data_structures.linked_list import LinkedList, DoublyLinkedList
from data_structures.binary_tree import BinarySearchTree
from data_structures.graph import Graph
from data_structures.heap import MinHeap, MaxHeap, PriorityQueue


def test_linked_list():
    """Test LinkedList implementation."""
    ll = LinkedList()

    # Test insertion
    ll.insert_at_head(3)
    ll.insert_at_head(2)
    ll.insert_at_head(1)
    ll.insert_at_tail(4)

    assert list(ll) == [1, 2, 3, 4]
    assert len(ll) == 4

    # Test search
    assert ll.search(3) is not None
    assert ll.search(10) is None

    # Test deletion
    assert ll.delete(2) == True
    assert list(ll) == [1, 3, 4]
    assert ll.delete(10) == False

    # Test reverse
    ll.reverse()
    assert list(ll) == [4, 3, 1]

    print("✓ LinkedList tests passed")


def test_binary_search_tree():
    """Test BinarySearchTree implementation."""
    bst = BinarySearchTree()

    # Test insertion
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(9)

    assert len(bst) == 5
    assert 7 in bst
    assert 10 not in bst

    # Test traversal
    assert bst.inorder_traversal() == [1, 3, 5, 7, 9]

    # Test search
    assert bst.search(7) is not None
    assert bst.search(10) is None

    # Test min/max
    assert bst.find_min().data == 1
    assert bst.find_max().data == 9

    # Test deletion
    bst.delete(3)
    assert 3 not in bst
    assert bst.inorder_traversal() == [1, 5, 7, 9]

    # Test validation
    assert bst.is_valid_bst() == True

    print("✓ BinarySearchTree tests passed")


def test_graph():
    """Test Graph implementation."""
    # Test undirected graph
    g = Graph(directed=False)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert len(g) == 4
    assert g.has_edge(0, 1) == True
    assert g.has_edge(1, 0) == True  # Undirected
    assert g.has_edge(0, 3) == False

    # Test BFS
    bfs_result = g.bfs(0)
    assert 0 in bfs_result
    assert len(bfs_result) == 4

    # Test DFS
    dfs_result = g.dfs(0)
    assert len(dfs_result) == 4

    # Test directed graph
    dg = Graph(directed=True)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    dg.add_edge(2, 0)

    assert dg.has_cycle() == True

    print("✓ Graph tests passed")


def test_heap():
    """Test heap implementations."""
    # Test MinHeap
    min_heap = MinHeap([5, 3, 7, 1, 9])
    assert min_heap.peek() == 1
    assert min_heap.pop() == 1
    assert min_heap.peek() == 3

    min_heap.push(2)
    assert min_heap.peek() == 2

    # Test MaxHeap
    max_heap = MaxHeap([5, 3, 7, 1, 9])
    assert max_heap.peek() == 9
    assert max_heap.pop() == 9
    assert max_heap.peek() == 7

    # Test PriorityQueue
    pq = PriorityQueue()
    pq.enqueue("task1", priority=3)
    pq.enqueue("task2", priority=1)
    pq.enqueue("task3", priority=2)

    assert pq.dequeue() == "task2"
    assert pq.dequeue() == "task3"
    assert pq.dequeue() == "task1"

    print("✓ Heap tests passed")


if __name__ == "__main__":
    test_linked_list()
    test_binary_search_tree()
    test_graph()
    test_heap()
    print("\n✓ All data structure tests passed!")
