"""
Binary Tree and Binary Search Tree Implementation

Provides tree data structures with various traversal methods.
"""

from typing import Any, Optional, List, Callable
from collections import deque


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, data: Any):
        self.data = data
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.data})"


class BinaryTree:
    """
    Binary Tree implementation.

    A tree data structure where each node has at most two children.
    """

    def __init__(self, root_data: Optional[Any] = None):
        self.root = TreeNode(root_data) if root_data is not None else None

    def inorder_traversal(self, node: Optional[TreeNode] = None, result: Optional[List] = None) -> List[Any]:
        """
        Inorder traversal (Left, Root, Right).
        Returns elements in sorted order for BST.
        """
        # Initialize result list on first call
        first_call = result is None
        if result is None:
            result = []
            node = self.root

        # Base case: empty node
        if node is None:
            return result

        # Recursive traversal
        self.inorder_traversal(node.left, result)
        result.append(node.data)
        self.inorder_traversal(node.right, result)

        return result

    def preorder_traversal(self, node: Optional[TreeNode] = None, result: Optional[List] = None) -> List[Any]:
        """Preorder traversal (Root, Left, Right)."""
        # Initialize result list on first call
        if result is None:
            result = []
            node = self.root

        # Base case: empty node
        if node is None:
            return result

        # Recursive traversal
        result.append(node.data)
        self.preorder_traversal(node.left, result)
        self.preorder_traversal(node.right, result)

        return result

    def postorder_traversal(self, node: Optional[TreeNode] = None, result: Optional[List] = None) -> List[Any]:
        """Postorder traversal (Left, Right, Root)."""
        # Initialize result list on first call
        if result is None:
            result = []
            node = self.root

        # Base case: empty node
        if node is None:
            return result

        # Recursive traversal
        self.postorder_traversal(node.left, result)
        self.postorder_traversal(node.right, result)
        result.append(node.data)

        return result

    def level_order_traversal(self) -> List[Any]:
        """
        Level-order traversal (breadth-first).
        Returns elements level by level from top to bottom.
        """
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def height(self, node: Optional[TreeNode] = None) -> int:
        """Calculate the height of the tree."""
        if node is None:
            node = self.root

        if not node:
            return 0

        left_height = self.height(node.left)
        right_height = self.height(node.right)

        return 1 + max(left_height, right_height)

    def __repr__(self) -> str:
        return f"BinaryTree(root={self.root.data if self.root else None})"


class BinarySearchTree(BinaryTree):
    """
    Binary Search Tree implementation.

    A binary tree where for each node:
    - All values in left subtree are less than node's value
    - All values in right subtree are greater than node's value

    Time Complexity (average case):
        - Search: O(log n)
        - Insert: O(log n)
        - Delete: O(log n)

    Time Complexity (worst case - unbalanced):
        - Search: O(n)
        - Insert: O(n)
        - Delete: O(n)
    """

    def __init__(self):
        super().__init__()
        self._size = 0

    def insert(self, data: Any) -> None:
        """Insert a new value into the BST."""
        if not self.root:
            self.root = TreeNode(data)
            self._size += 1
            return

        # Check if value already exists (no duplicates)
        if self.search(data) is not None:
            return

        self.root = self._insert_recursive(self.root, data)
        self._size += 1

    def _insert_recursive(self, node: Optional[TreeNode], data: Any) -> TreeNode:
        """Helper method for recursive insertion."""
        if not node:
            return TreeNode(data)

        if data < node.data:
            node.left = self._insert_recursive(node.left, data)
        elif data > node.data:
            node.right = self._insert_recursive(node.right, data)
        # If data == node.data, don't insert (no duplicates)

        return node

    def search(self, data: Any) -> Optional[TreeNode]:
        """Search for a value in the BST."""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: Optional[TreeNode], data: Any) -> Optional[TreeNode]:
        """Helper method for recursive search."""
        if not node or node.data == data:
            return node

        if data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def find_min(self, node: Optional[TreeNode] = None) -> Optional[TreeNode]:
        """Find the node with minimum value."""
        if node is None:
            node = self.root

        if not node:
            return None

        while node.left:
            node = node.left
        return node

    def find_max(self, node: Optional[TreeNode] = None) -> Optional[TreeNode]:
        """Find the node with maximum value."""
        if node is None:
            node = self.root

        if not node:
            return None

        while node.right:
            node = node.right
        return node

    def delete(self, data: Any) -> None:
        """Delete a value from the BST."""
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node: Optional[TreeNode], data: Any) -> Optional[TreeNode]:
        """Helper method for recursive deletion."""
        if not node:
            return None

        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            # Node to delete found
            # Case 1: No children or one child
            if not node.left:
                self._size -= 1
                return node.right
            elif not node.right:
                self._size -= 1
                return node.left

            # Case 2: Two children
            # Find inorder successor (min value in right subtree)
            successor = self.find_min(node.right)
            node.data = successor.data
            node.right = self._delete_recursive(node.right, successor.data)

        return node

    def is_valid_bst(self, node: Optional[TreeNode] = None, min_val: float = float('-inf'), max_val: float = float('inf')) -> bool:
        """Validate that the tree is a valid BST."""
        # Use root if this is the initial call (no node specified)
        if node is None and min_val == float('-inf') and max_val == float('inf'):
            node = self.root

        # Base case: empty node is valid
        if node is None:
            return True

        # Check if current node violates BST property
        if node.data <= min_val or node.data >= max_val:
            return False

        # Recursively validate left and right subtrees
        return (self.is_valid_bst(node.left, min_val, node.data) and
                self.is_valid_bst(node.right, node.data, max_val))

    def __len__(self) -> int:
        return self._size

    def __contains__(self, data: Any) -> bool:
        return self.search(data) is not None

    def __repr__(self) -> str:
        return f"BinarySearchTree(size={self._size}, root={self.root.data if self.root else None})"
