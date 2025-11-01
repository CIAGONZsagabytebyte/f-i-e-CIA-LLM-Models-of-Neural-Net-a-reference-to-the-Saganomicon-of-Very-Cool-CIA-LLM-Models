"""
Graph Algorithms

Advanced graph algorithms including shortest path and minimum spanning tree.
"""

import heapq
from typing import Dict, List, Set, Optional, Tuple, Any
from collections import defaultdict, deque
import math


def dijkstra(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> Dict[Any, float]:
    """
    Dijkstra's shortest path algorithm.

    Finds shortest paths from start vertex to all other vertices.

    Time Complexity: O((V + E) log V) with binary heap
    Space Complexity: O(V)

    Args:
        graph: Adjacency list with weighted edges {vertex: [(neighbor, weight), ...]}
        start: Starting vertex

    Returns:
        Dictionary mapping vertices to shortest distance from start
    """
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    pq = [(0, start)]  # (distance, vertex)
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight

            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances


def dijkstra_path(graph: Dict[Any, List[Tuple[Any, float]]], start: Any, end: Any) -> Tuple[List[Any], float]:
    """
    Find shortest path between two vertices using Dijkstra's algorithm.

    Args:
        graph: Adjacency list with weighted edges
        start: Starting vertex
        end: Target vertex

    Returns:
        Tuple of (path, distance)
    """
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    previous = {start: None}

    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current == end:
            break

        if current in visited:
            continue

        visited.add(current)

        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight

            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    return path, distances[end]


def bellman_ford(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> Tuple[Dict[Any, float], bool]:
    """
    Bellman-Ford algorithm for shortest paths.

    Can handle negative edge weights and detect negative cycles.

    Time Complexity: O(V * E)
    Space Complexity: O(V)

    Args:
        graph: Adjacency list with weighted edges
        start: Starting vertex

    Returns:
        Tuple of (distances dict, has_negative_cycle)
    """
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    # Relax edges V-1 times
    vertices = list(graph.keys())
    for _ in range(len(vertices) - 1):
        for vertex in vertices:
            for neighbor, weight in graph.get(vertex, []):
                if distances[vertex] + weight < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distances[vertex] + weight

    # Check for negative cycles
    has_negative_cycle = False
    for vertex in vertices:
        for neighbor, weight in graph.get(vertex, []):
            if distances[vertex] + weight < distances.get(neighbor, float('inf')):
                has_negative_cycle = True
                break

    return distances, has_negative_cycle


def floyd_warshall(graph: Dict[Any, List[Tuple[Any, float]]]) -> Dict[Tuple[Any, Any], float]:
    """
    Floyd-Warshall algorithm for all-pairs shortest paths.

    Time Complexity: O(V³)
    Space Complexity: O(V²)

    Args:
        graph: Adjacency list with weighted edges

    Returns:
        Dictionary mapping (source, destination) to shortest distance
    """
    vertices = list(graph.keys())
    distances = {}

    # Initialize distances
    for i in vertices:
        for j in vertices:
            if i == j:
                distances[(i, j)] = 0
            else:
                distances[(i, j)] = float('inf')

    # Add edge weights
    for vertex in vertices:
        for neighbor, weight in graph.get(vertex, []):
            distances[(vertex, neighbor)] = weight

    # Floyd-Warshall main loop
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if distances[(i, k)] + distances[(k, j)] < distances[(i, j)]:
                    distances[(i, j)] = distances[(i, k)] + distances[(k, j)]

    return distances


def a_star(graph: Dict[Any, List[Tuple[Any, float]]],
           start: Any,
           goal: Any,
           heuristic: Dict[Any, float]) -> Tuple[List[Any], float]:
    """
    A* pathfinding algorithm.

    Uses heuristic to guide search toward goal.

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        graph: Adjacency list with weighted edges
        start: Starting vertex
        goal: Goal vertex
        heuristic: Dictionary mapping vertices to estimated distance to goal

    Returns:
        Tuple of (path, distance)
    """
    g_score = {vertex: float('inf') for vertex in graph}
    g_score[start] = 0

    f_score = {vertex: float('inf') for vertex in graph}
    f_score[start] = heuristic.get(start, 0)

    previous = {start: None}
    open_set = [(f_score[start], start)]
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = previous.get(current)
            path.reverse()
            return path, g_score[goal]

        if current in closed_set:
            continue

        closed_set.add(current)

        for neighbor, weight in graph.get(current, []):
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + weight

            if tentative_g < g_score.get(neighbor, float('inf')):
                previous[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic.get(neighbor, 0)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return [], float('inf')


def kruskal_mst(edges: List[Tuple[Any, Any, float]]) -> List[Tuple[Any, Any, float]]:
    """
    Kruskal's algorithm for minimum spanning tree.

    Time Complexity: O(E log E)
    Space Complexity: O(V)

    Args:
        edges: List of (vertex1, vertex2, weight) tuples

    Returns:
        List of edges in the MST
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])

    # Union-Find data structure
    parent = {}
    rank = {}

    def find(vertex):
        if vertex not in parent:
            parent[vertex] = vertex
            rank[vertex] = 0
        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])  # Path compression
        return parent[vertex]

    def union(v1, v2):
        root1 = find(v1)
        root2 = find(v2)

        if root1 == root2:
            return False

        # Union by rank
        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root2] = root1
            rank[root1] += 1

        return True

    mst = []

    for v1, v2, weight in sorted_edges:
        if union(v1, v2):
            mst.append((v1, v2, weight))

    return mst


def prim_mst(graph: Dict[Any, List[Tuple[Any, float]]]) -> List[Tuple[Any, Any, float]]:
    """
    Prim's algorithm for minimum spanning tree.

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        graph: Adjacency list with weighted edges

    Returns:
        List of edges in the MST
    """
    if not graph:
        return []

    vertices = list(graph.keys())
    start = vertices[0]

    mst = []
    visited = {start}
    edges = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(edges)

    while edges and len(visited) < len(vertices):
        weight, v1, v2 = heapq.heappop(edges)

        if v2 in visited:
            continue

        visited.add(v2)
        mst.append((v1, v2, weight))

        for neighbor, edge_weight in graph.get(v2, []):
            if neighbor not in visited:
                heapq.heappush(edges, (edge_weight, v2, neighbor))

    return mst


def topological_sort_kahn(graph: Dict[Any, List[Any]]) -> Optional[List[Any]]:
    """
    Topological sort using Kahn's algorithm (iterative).

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Args:
        graph: Adjacency list representing a directed acyclic graph

    Returns:
        Topologically sorted list of vertices, or None if cycle exists
    """
    # Calculate in-degrees
    in_degree = {vertex: 0 for vertex in graph}

    for vertex in graph:
        for neighbor in graph[vertex]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1

    # Queue of vertices with in-degree 0
    queue = deque([v for v in in_degree if in_degree[v] == 0])
    result = []

    while queue:
        vertex = queue.popleft()
        result.append(vertex)

        for neighbor in graph.get(vertex, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all vertices were processed (no cycle)
    if len(result) == len(in_degree):
        return result
    else:
        return None  # Cycle detected


def strongly_connected_components(graph: Dict[Any, List[Any]]) -> List[Set[Any]]:
    """
    Find strongly connected components using Kosaraju's algorithm.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Args:
        graph: Adjacency list representing a directed graph

    Returns:
        List of sets, each containing vertices in a strongly connected component
    """
    # First DFS to get finishing times
    visited = set()
    stack = []

    def dfs1(vertex):
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs1(neighbor)
        stack.append(vertex)

    for vertex in graph:
        if vertex not in visited:
            dfs1(vertex)

    # Create transpose graph
    transpose = defaultdict(list)
    for vertex in graph:
        for neighbor in graph[vertex]:
            transpose[neighbor].append(vertex)

    # Second DFS on transpose graph
    visited.clear()
    sccs = []

    def dfs2(vertex, component):
        visited.add(vertex)
        component.add(vertex)
        for neighbor in transpose.get(vertex, []):
            if neighbor not in visited:
                dfs2(neighbor, component)

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            component = set()
            dfs2(vertex, component)
            sccs.append(component)

    return sccs
