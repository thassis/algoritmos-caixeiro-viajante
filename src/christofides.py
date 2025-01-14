import networkx as nx

def eulerian_tour(mst, matching):
    multigraph = nx.MultiGraph(mst)
    for u, v in matching:
        multigraph.add_edge(u, v, weight=0)
    return list(nx.eulerian_circuit(multigraph))

def shortcut_tour(tour):
    path = []
    visited = set()
    for u, v in tour:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])
    return path

def christofides_tsp(graph):
    mst = nx.minimum_spanning_tree(graph)
    
    odd_vertices = [v for v, degree in mst.degree() if degree % 2 == 1]

    subgraph = graph.subgraph(odd_vertices)
    matching = nx.algorithms.matching.max_weight_matching(subgraph, maxcardinality=True)
    
    tour = eulerian_tour(mst, matching)
    path = shortcut_tour(tour)

    total_cost = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

    return total_cost, path
