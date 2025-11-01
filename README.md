# Computer Science Fundamentals

A comprehensive collection of computer science fundamentals including data structures, algorithms, and mathematical utilities implemented in Python.

## Structure

```
.
├── data_structures/    # Core data structure implementations
├── algorithms/         # Classic algorithms (sorting, searching, graph algorithms)
├── math_utils/         # Mathematical utilities and computational methods
├── examples/          # Usage examples and demonstrations
└── tests/             # Unit tests
```

## Features

### Data Structures
- Linked Lists (Singly, Doubly)
- Trees (Binary, BST, AVL)
- Graphs (Adjacency List, Adjacency Matrix)
- Heaps (Min, Max)
- Hash Tables
- Stacks and Queues

### Algorithms
- Sorting (QuickSort, MergeSort, HeapSort)
- Searching (Binary Search, DFS, BFS)
- Dynamic Programming
- Graph Algorithms (Dijkstra, A*, Floyd-Warshall)

### Mathematical Utilities
- Natural logarithm operations
- Statistical functions
- Numerical methods
- Matrix operations

## Usage

Each module is self-contained with documentation and examples.

```python
from data_structures.binary_tree import BinarySearchTree
from algorithms.sorting import quick_sort
from math_utils.logarithms import natural_log

# Example usage
tree = BinarySearchTree()
tree.insert(5)
tree.insert(3)
tree.insert(7)

sorted_array = quick_sort([3, 1, 4, 1, 5, 9, 2, 6])
log_value = natural_log(2.718281828)
```

## Installation

```bash
pip install -r requirements.txt
```

## Testing

```bash
python -m pytest tests/
```

## License

MIT License
