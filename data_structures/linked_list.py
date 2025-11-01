"""
Linked List Implementation

Provides singly and doubly linked list data structures.
"""

from typing import Any, Optional, Iterator


class Node:
    """A node in a singly linked list."""

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class LinkedList:
    """
    Singly Linked List implementation.

    A linear data structure where elements are stored in nodes,
    each pointing to the next node in the sequence.

    Time Complexity:
        - Access: O(n)
        - Search: O(n)
        - Insert (at head): O(1)
        - Delete (at head): O(1)
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0

    def insert_at_head(self, data: Any) -> None:
        """Insert a new node at the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Insert a new node at the end of the list."""
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self._size += 1
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self._size += 1

    def delete(self, data: Any) -> bool:
        """
        Delete the first node with the given data.
        Returns True if successful, False if not found.
        """
        if not self.head:
            return False

        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next

        return False

    def search(self, data: Any) -> Optional[Node]:
        """Search for a node with the given data."""
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

    def reverse(self) -> None:
        """Reverse the linked list in place."""
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        elements = list(self)
        return f"LinkedList({elements})"


class DoublyNode:
    """A node in a doubly linked list."""

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[DoublyNode] = None
        self.prev: Optional[DoublyNode] = None

    def __repr__(self) -> str:
        return f"DoublyNode({self.data})"


class DoublyLinkedList:
    """
    Doubly Linked List implementation.

    Each node has references to both next and previous nodes,
    allowing bidirectional traversal.

    Time Complexity:
        - Access: O(n)
        - Search: O(n)
        - Insert (at head/tail): O(1)
        - Delete (with node reference): O(1)
    """

    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size = 0

    def insert_at_head(self, data: Any) -> None:
        """Insert a new node at the beginning."""
        new_node = DoublyNode(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Insert a new node at the end."""
        new_node = DoublyNode(data)

        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def delete_node(self, node: DoublyNode) -> None:
        """Delete a specific node."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self._size -= 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        elements = list(self)
        return f"DoublyLinkedList({elements})"
