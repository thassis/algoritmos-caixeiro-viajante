import networkx as nx
import math
import heapq

def read_tsp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not any("TSP" in line for line in lines):
        print("Arquivo não contém especificação TSP")
        return
    if not any("EUC_2D" in line for line in lines):
        print("Arquivo não contém coordenadas EUC_2D")
        return

    G = nx.Graph()
    coords = {}
    reading_coords = False

    for line in lines:
        if line.startswith("NODE_COORD_SECTION"):
            reading_coords = True
            continue
        elif line.startswith("EOF"):
            break

        if reading_coords:
            parts = line.split()
            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            coords[node_id] = (x, y)
            G.add_node(node_id, pos=(x, y))

    for i in coords:
        for j in coords:
            # nint( sqrt( xd*xd + yd*yd) );
            distance = int((((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2) ** 0.5) + 0.5)
            G.add_edge(i, j, weight=distance)

    return G

def bound(path, graph, n):
    total_cost = 0
    included_edges = set(zip(path[:-1], path[1:]))  # Arestas já incluídas no caminho
    
    reverse_edges = {(v, u) for u, v in included_edges}
    included_edges.update(reverse_edges)
    
    for i in range(n):
        if i in path and i != path[-1]:
            # Se o vértice já foi visitado (exceto o último), ignora
            continue

        neighbors = []
        for j in range(n):
            if i != j:
                # Verifica se a aresta (i, j) não está bloqueada e coleta os custos
                if (i, j) not in included_edges:
                    neighbors.append(graph[i][j])

        # Ordena os custos das arestas incidentes e soma os menores dois
        neighbors = sorted(neighbors)
        if len(neighbors) > 1:
            total_cost += neighbors[0] + neighbors[1]
        elif neighbors:
            total_cost += neighbors[0]

    # Adiciona o custo das arestas já incluídas no caminho
    for u, v in included_edges:
        total_cost += graph[u][v]

    # print(math.ceil(total_cost / 2), path)
    return math.ceil(total_cost / 2)


def bnb_tsp(graph, n):
    root = (bound([0], graph, n), 0, 0, [0])  # (bound, level, cost, path)
    queue = []
    heapq.heappush(queue, root)
    best = math.inf
    sol = None
    
    while queue:
        node = heapq.heappop(queue)
        node_bound, node_level, node_cost, node_path = node
        if node_level > n-1:
            if best > node_cost:
                best = node_cost
                sol = node_path
                print(best, sol, node_level)
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
    
    return best, sol


if __name__ == "__main__":
    G = read_tsp_file('tsp_examples/eil51.tsp')
    # Cria um grafo não direcionado
    # G = nx.Graph()

    # Adiciona as arestas e seus respectivos pesos
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

    # print("Graph constructed with nodes:", G.nodes())
    # print("Graph constructed with edges:", G.edges(data=True))
    
    A = nx.adjacency_matrix(G).toarray()
    # Número de nós
    n = len(G.nodes)
    solution, cost = bnb_tsp(A, n)
    # print("Melhor caminho:", solution)
    # print("Custo mínimo:", cost)

