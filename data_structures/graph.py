"""
Graph Implementation

Provides graph data structures with adjacency list and matrix representations.
"""

from typing import Any, Dict, List, Set, Optional
from collections import defaultdict, deque


class Graph:
    """
    Graph implementation using adjacency list.

    Can represent both directed and undirected graphs.

    Time Complexity:
        - Add vertex: O(1)
        - Add edge: O(1)
        - Remove vertex: O(V + E)
        - Remove edge: O(E)
        - Query edge: O(V) worst case, O(1) average
    """

    def __init__(self, directed: bool = False):
        self.graph: Dict[Any, List[Any]] = defaultdict(list)
        self.directed = directed
        self._vertices: Set[Any] = set()

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        if vertex not in self._vertices:
            self._vertices.add(vertex)
            if vertex not in self.graph:
                self.graph[vertex] = []

    def add_edge(self, src: Any, dest: Any, weight: Optional[float] = None) -> None:
        """
        Add an edge between two vertices.

        For undirected graphs, adds edges in both directions.
        """
        self.add_vertex(src)
        self.add_vertex(dest)

        # Store as tuple (destination, weight) if weighted
        if weight is not None:
            self.graph[src].append((dest, weight))
            if not self.directed:
                self.graph[dest].append((src, weight))
        else:
            self.graph[src].append(dest)
            if not self.directed:
                self.graph[dest].append(src)

    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its edges."""
        if vertex not in self._vertices:
            return

        # Remove all edges to this vertex
        for v in self._vertices:
            if v != vertex:
                self.graph[v] = [edge for edge in self.graph[v] if edge != vertex]

        # Remove the vertex itself
        del self.graph[vertex]
        self._vertices.remove(vertex)

    def remove_edge(self, src: Any, dest: Any) -> None:
        """Remove an edge between two vertices."""
        if src in self.graph:
            self.graph[src] = [edge for edge in self.graph[src] if edge != dest]

        if not self.directed and dest in self.graph:
            self.graph[dest] = [edge for edge in self.graph[dest] if edge != src]

    def get_neighbors(self, vertex: Any) -> List[Any]:
        """Get all neighbors of a vertex."""
        return self.graph.get(vertex, [])

    def has_edge(self, src: Any, dest: Any) -> bool:
        """Check if an edge exists between two vertices."""
        return dest in self.graph.get(src, [])

    def dfs(self, start: Any, visited: Optional[Set] = None) -> List[Any]:
        """
        Depth-First Search traversal.

        Time Complexity: O(V + E)
        """
        if visited is None:
            visited = set()

        result = []

        def dfs_recursive(vertex: Any):
            visited.add(vertex)
            result.append(vertex)

            for neighbor in self.graph.get(vertex, []):
                # Handle weighted edges
                next_vertex = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                if next_vertex not in visited:
                    dfs_recursive(next_vertex)

        dfs_recursive(start)
        return result

    def bfs(self, start: Any) -> List[Any]:
        """
        Breadth-First Search traversal.

        Time Complexity: O(V + E)
        """
        visited = {start}
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.graph.get(vertex, []):
                # Handle weighted edges
                next_vertex = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                if next_vertex not in visited:
                    visited.add(next_vertex)
                    queue.append(next_vertex)

        return result

    def has_cycle(self) -> bool:
        """
        Detect if the graph contains a cycle.

        For directed graphs, uses DFS with recursion stack.
        For undirected graphs, uses DFS with parent tracking.
        """
        visited = set()

        def has_cycle_directed(vertex: Any, rec_stack: Set) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor in self.graph.get(vertex, []):
                next_vertex = neighbor[0] if isinstance(neighbor, tuple) else neighbor

                if next_vertex not in visited:
                    if has_cycle_directed(next_vertex, rec_stack):
                        return True
                elif next_vertex in rec_stack:
                    return True

            rec_stack.remove(vertex)
            return False

        def has_cycle_undirected(vertex: Any, parent: Any) -> bool:
            visited.add(vertex)

            for neighbor in self.graph.get(vertex, []):
                next_vertex = neighbor[0] if isinstance(neighbor, tuple) else neighbor

                if next_vertex not in visited:
                    if has_cycle_undirected(next_vertex, vertex):
                        return True
                elif next_vertex != parent:
                    return True

            return False

        for vertex in self._vertices:
            if vertex not in visited:
                if self.directed:
                    if has_cycle_directed(vertex, set()):
                        return True
                else:
                    if has_cycle_undirected(vertex, None):
                        return True

        return False

    def topological_sort(self) -> Optional[List[Any]]:
        """
        Topological sort of the graph (only for DAGs).

        Returns None if the graph has a cycle.
        Time Complexity: O(V + E)
        """
        if not self.directed or self.has_cycle():
            return None

        visited = set()
        stack = []

        def dfs_topo(vertex: Any):
            visited.add(vertex)

            for neighbor in self.graph.get(vertex, []):
                next_vertex = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                if next_vertex not in visited:
                    dfs_topo(next_vertex)

            stack.append(vertex)

        for vertex in self._vertices:
            if vertex not in visited:
                dfs_topo(vertex)

        return stack[::-1]

    @property
    def vertices(self) -> Set[Any]:
        """Get all vertices in the graph."""
        return self._vertices.copy()

    @property
    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        count = sum(len(edges) for edges in self.graph.values())
        return count if self.directed else count // 2

    def __len__(self) -> int:
        """Return the number of vertices."""
        return len(self._vertices)

    def __repr__(self) -> str:
        return f"Graph(vertices={len(self._vertices)}, edges={self.edge_count}, directed={self.directed})"

    def __str__(self) -> str:
        """String representation showing all edges."""
        lines = [f"Graph ({'Directed' if self.directed else 'Undirected'}):"]
        for vertex in sorted(self._vertices):
            neighbors = self.graph[vertex]
            lines.append(f"  {vertex} -> {neighbors}")
        return "\n".join(lines)
