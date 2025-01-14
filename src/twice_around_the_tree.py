import networkx as nx
import tracemalloc
from utils import read_tsp_file

def twice_around_the_tree_tsp(file):
    tracemalloc.start()
    G = read_tsp_file(file)
    root = list(G.nodes())[0]
    
    mst = nx.minimum_spanning_tree(G, algorithm="prim", weight="weight")
    
    preorder_nodes = list(nx.dfs_preorder_nodes(mst, source=root))
    
    hamiltonian_cycle = preorder_nodes + [preorder_nodes[0]]  # Retornar ao ponto inicial
    
    total_cost = 0
    for i in range(len(hamiltonian_cycle) - 1):
        u, v = hamiltonian_cycle[i], hamiltonian_cycle[i + 1]
        total_cost += G[u][v]["weight"]
    
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return total_cost, hamiltonian_cycle, memory_usage
