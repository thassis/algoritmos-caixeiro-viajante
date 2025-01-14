import math
import heapq
import tracemalloc
import networkx as nx
from collections import deque
from utils import read_tsp_file

def bound(path, graph, n):
    total_cost = 0
    visited_edges = [[False] * n for _ in range(n)]
    for u, v in zip(path[:-1], path[1:]):
        visited_edges[u][v] = visited_edges[v][u] = True
        total_cost += graph[u][v]

    for i in range(n):
        if i in path and i != path[-1]:
            continue

        min1, min2 = math.inf, math.inf
        for j in range(n):
            if i != j and not visited_edges[i][j]:
                cost = graph[i][j]
                if cost < min1:
                    min1, min2 = cost, min1
                elif cost < min2:
                    min2 = cost

        if min1 < math.inf:
            total_cost += min1
        if min2 < math.inf:
            total_cost += min2

    return math.ceil(total_cost / 2)


def bnb_tsp(file):
    tracemalloc.start()
    G = read_tsp_file(file)
    graph = nx.adjacency_matrix(G).toarray()
    n = len(G.nodes)
    del G
    root = (bound([0], graph, n), 0, 0, [0])  # (bound, level, cost, path)
    queue = []
    heapq.heappush(queue, root)
    best = math.inf
    path = None
    
    while queue:
        node = heapq.heappop(queue)
        node_bound, node_level, node_cost, node_path = node
        if node_level > n-1:
            if best > node_cost:
                best = node_cost
                path = node_path
                # print(best, path, node_level)
        elif node_bound < best:
            if node_level < n-1:
                for k in range(1, n):
                    if k not in node_path and graph[node_path[-1]][k] != math.inf:
                        new_path = node_path + [k]
                        new_bound = bound(new_path, graph, n)
                        if new_bound < best:
                            heapq.heappush(queue, (new_bound, node_level + 1, node_cost + graph[node_path[-1]][k], new_path))
            elif graph[node_path[-1]][0] != math.inf:
                new_path = node_path + [0]
                new_bound = bound(new_path, graph, n)
                if new_bound < best and all(i in node_path for i in range(n)):
                    heapq.heappush(queue, (new_bound, node_level + 1, node_cost + graph[node_path[-1]][0], new_path))
    
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return best, path, memory_usage

def bfs_tsp(file):
    tracemalloc.start()
    
    graph = read_tsp_file(file)
    n = len(graph.nodes)
    queue = deque([(0, 0, [0])])  # (cost, level, path)
    best = math.inf
    path = None

    while queue:
        cost, level, path = queue.popleft()

        if level == n - 1:
            # Check if we can return to the starting node to complete the cycle
            if graph[path[-1]][0] != math.inf:
                total_cost = cost + graph[path[-1]][0]
                if total_cost < best:
                    best = total_cost
                    path = path + [0]
        else:
            # Expand all possible next nodes that are not in the path
            for next_node in range(1, n):
                if next_node not in path and graph[path[-1]][next_node] != math.inf:
                    new_cost = cost + graph[path[-1]][next_node]
                    new_path = path + [next_node]
                    queue.append((new_cost, level + 1, new_path))
 
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return best, path, memory_usage