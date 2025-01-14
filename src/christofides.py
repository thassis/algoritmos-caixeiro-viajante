import networkx as nx
import tracemalloc
from networkx.algorithms import matching

def christofides_tsp(graph):
    tracemalloc.start()
    # Etapa 1: Computar a Árvore Geradora Mínima (AGM)
    mst = nx.minimum_spanning_tree(graph)

    # Etapa 2: Selecionar vértices de grau ímpar
    odd_vertices = [node for node, degree in mst.degree() if degree % 2 == 1]

    # Subgrafo induzido pelos vértices de grau ímpar
    odd_subgraph = graph.subgraph(odd_vertices)

    # Computar o emparelhamento perfeito de custo mínimo
    perfect_matching = nx.min_weight_matching(odd_subgraph)

    # Criar multigrafo unindo AGM e emparelhamento
    multi_graph = nx.MultiGraph(mst)
    multi_graph.add_edges_from(
        [(u, v, {'weight': graph[u][v]['weight']}) for u, v in perfect_matching]
    )

    # Computar o circuito euleriano no multigrafo
    eulerian_circuit = [u for u, _ in nx.eulerian_circuit(multi_graph)]

    # Remover vértices duplicados para formar o caminho Hamiltoniano
    hamiltonian_path = list(dict.fromkeys(eulerian_circuit))
    hamiltonian_path.append(hamiltonian_path[0])  # Fechar o ciclo

    # Calcular o custo total do caminho
    total_cost = sum(
        graph[hamiltonian_path[i]][hamiltonian_path[i + 1]]['weight']
        for i in range(len(hamiltonian_path) - 1)
    )

    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return total_cost, hamiltonian_path, memory_usage
