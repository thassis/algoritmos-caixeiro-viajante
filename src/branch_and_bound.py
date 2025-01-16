import math
import heapq
import tracemalloc
import logging
import networkx as nx
from collections import deque
from utils import read_tsp_file
# Configuração do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

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
    # G = nx.Graph()
    # edges = [
    #     (1, 2, 3),
    #     (1, 3, 1),
    #     (1, 4, 5),
    #     (1, 5, 8),
    #     (2, 4, 7),
    #     (2, 3, 6),
    #     (2, 5, 9),
    #     (3, 4, 4),
    #     (3, 5, 2),
    #     (4, 5, 3)
    # ]
    # G.add_weighted_edges_from(edges)
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

        if node_level > n - 1:
            if best > node_cost:
                best = node_cost
                path = node_path
                # logging.debug(f"Solução encontrada com custo {best}, caminho {path}")
        elif node_bound < best:
            if node_level < n - 1:
                for k in range(1, n):
                    if k not in node_path and graph[node_path[-1]][k] != math.inf:
                        new_path = node_path + [k]
                        new_bound = bound(new_path, graph, n)
                        if new_bound < best:
                            # logging.debug(f"Explorando caminho {new_path} com novo limite inferior {new_bound}")
                            heapq.heappush(queue, (new_bound, node_level + 1, node_cost + graph[node_path[-1]][k], new_path))
            elif graph[node_path[-1]][0] != math.inf:
                new_path = node_path + [0]
                new_bound = bound(new_path, graph, n)
                if new_bound < best and all(i in node_path for i in range(n)):
                    # logging.debug(f"Explorando caminho completo {new_path} com novo limite inferior {new_bound}")
                    heapq.heappush(queue, (new_bound, node_level + 1, node_cost + graph[node_path[-1]][0], new_path))
            else:
                logging.debug(f"Poda do nó com caminho {node_path} devido ao custo")
        else:
            logging.debug(f"Poda do nó com caminho {node_path} devido ao limite inferior")
    
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return best, path, memory_usage

def bfs_tsp(file):
    def dfs_with_bound(path, graph, n, best_cost, best_path):
        current_cost = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
        # logging.debug(f"Próximo caminho: {path} custo: {current_cost}")

        if len(path) == n and graph[path[-1]][0] != math.inf:
            current_cost += graph[path[-1]][0]
            # logging.debug(f"Caminho completo: {path + [0]} | custo: {current_cost}")
            if current_cost < best_cost:
                return current_cost, path + [0]
            return best_cost, best_path

        current_bound = bound(path, graph, n)
        # logging.debug(f"Caminho: {path} bound: {current_bound}")

        if current_bound >= best_cost:
            # logging.debug(f"Poda do nó com caminho {path} devido ao limite inferior ({best_cost})")
            return best_cost, best_path

        for k in range(1, n):
            if k not in path and graph[path[-1]][k] != math.inf:
                new_cost, new_path = dfs_with_bound(path + [k], graph, n, best_cost, best_path)
                if new_cost < best_cost:
                    # logging.debug(f"Novo melhor caminho: {new_path} com custo: {new_cost}")
                    best_cost, best_path = new_cost, new_path

        return best_cost, best_path

    tracemalloc.start()

    G = read_tsp_file(file)
    # G = nx.Graph()
    # edges = [
    #     (1, 2, 3),
    #     (1, 3, 1),
    #     (1, 4, 5),
    #     (1, 5, 8),
    #     (2, 4, 7),
    #     (2, 3, 6),
    #     (2, 5, 9),
    #     (3, 4, 4),
    #     (3, 5, 2),
    #     (4, 5, 3)
    # ]
    # G.add_weighted_edges_from(edges)
    graph = nx.adjacency_matrix(G).toarray()
    n = len(G.nodes)
    del G

    best_cost, best_path = dfs_with_bound([0], graph, n, math.inf, None)

    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return best_cost, best_path, memory_usage
