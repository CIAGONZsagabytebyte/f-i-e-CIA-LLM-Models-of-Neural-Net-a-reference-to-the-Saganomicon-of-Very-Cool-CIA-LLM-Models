"""
Example usage of the computer science fundamentals library.
"""

import sys
sys.path.insert(0, '..')

from data_structures.linked_list import LinkedList
from data_structures.binary_tree import BinarySearchTree
from data_structures.graph import Graph
from data_structures.heap import PriorityQueue

from algorithms.sorting import quick_sort, merge_sort
from algorithms.searching import binary_search
from algorithms.graph_algorithms import dijkstra, kruskal_mst

from math_utils.logarithms import natural_log, exp
from math_utils.statistics import mean, standard_deviation, correlation
from math_utils.numerical_methods import newton_raphson, simpsons_rule


def example_data_structures():
    """Demonstrate data structure usage."""
    print("=== Data Structures Examples ===\n")

    # Linked List
    print("1. Linked List:")
    ll = LinkedList()
    for i in [5, 3, 7, 1, 9]:
        ll.insert_at_tail(i)
    print(f"   List: {list(ll)}")
    ll.reverse()
    print(f"   Reversed: {list(ll)}\n")

    # Binary Search Tree
    print("2. Binary Search Tree:")
    bst = BinarySearchTree()
    for value in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(value)
    print(f"   Inorder traversal: {bst.inorder_traversal()}")
    print(f"   Contains 40: {40 in bst}")
    print(f"   Min value: {bst.find_min().data}")
    print(f"   Max value: {bst.find_max().data}\n")

    # Graph
    print("3. Graph:")
    g = Graph(directed=False)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'D')
    print(f"   BFS from A: {g.bfs('A')}")
    print(f"   DFS from A: {g.dfs('A')}")
    print(f"   Has cycle: {g.has_cycle()}\n")

    # Priority Queue
    print("4. Priority Queue:")
    pq = PriorityQueue()
    pq.enqueue("Low priority task", priority=3)
    pq.enqueue("High priority task", priority=1)
    pq.enqueue("Medium priority task", priority=2)
    print(f"   First dequeue: {pq.dequeue()}")
    print(f"   Second dequeue: {pq.dequeue()}")
    print(f"   Third dequeue: {pq.dequeue()}\n")


def example_algorithms():
    """Demonstrate algorithm usage."""
    print("=== Algorithms Examples ===\n")

    # Sorting
    print("1. Sorting:")
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Unsorted: {unsorted}")
    print(f"   Quick sort: {quick_sort(unsorted)}")
    print(f"   Merge sort: {merge_sort(unsorted)}\n")

    # Searching
    print("2. Searching:")
    sorted_array = [11, 12, 22, 25, 34, 64, 90]
    target = 25
    index = binary_search(sorted_array, target)
    print(f"   Array: {sorted_array}")
    print(f"   Binary search for {target}: index {index}\n")

    # Graph Algorithms
    print("3. Shortest Path (Dijkstra):")
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8)],
        'D': [('B', 5), ('C', 8)]
    }
    distances = dijkstra(graph, 'A')
    print(f"   Shortest distances from A: {distances}\n")

    # Minimum Spanning Tree
    print("4. Minimum Spanning Tree (Kruskal):")
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8)
    ]
    mst = kruskal_mst(edges)
    print(f"   MST edges: {mst}")
    print(f"   Total weight: {sum(w for _, _, w in mst)}\n")


def example_math_utils():
    """Demonstrate mathematical utilities."""
    print("=== Mathematical Utilities Examples ===\n")

    # Logarithms
    print("1. Logarithms:")
    print(f"   ln(e) = {natural_log(2.718281828):.6f}")
    print(f"   e^2 = {exp(2):.6f}\n")

    # Statistics
    print("2. Statistics:")
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    print(f"   Data: {data}")
    print(f"   Mean: {mean(data)}")
    print(f"   Standard deviation: {standard_deviation(data):.4f}\n")

    # Correlation
    print("3. Correlation:")
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    corr = correlation(x, y)
    print(f"   X: {x}")
    print(f"   Y: {y}")
    print(f"   Correlation: {corr:.4f}\n")

    # Numerical Methods - Root Finding
    print("4. Root Finding (Newton-Raphson):")
    print("   Finding square root of 10:")
    f = lambda x: x**2 - 10
    df = lambda x: 2*x
    root, iterations = newton_raphson(f, df, 3.0)
    print(f"   Root: {root:.6f} (in {iterations} iterations)")
    print(f"   Verification: {root**2:.6f}\n")

    # Numerical Integration
    print("5. Numerical Integration (Simpson's Rule):")
    print("   Computing ∫₀¹ x² dx:")
    f = lambda x: x**2
    result = simpsons_rule(f, 0, 1, n=100)
    print(f"   Numerical result: {result:.6f}")
    print(f"   Analytical result: {1/3:.6f}\n")


def main():
    """Run all examples."""
    print("=" * 50)
    print("Computer Science Fundamentals - Examples")
    print("=" * 50)
    print()

    example_data_structures()
    print()
    example_algorithms()
    print()
    example_math_utils()

    print("=" * 50)
    print("Examples completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
