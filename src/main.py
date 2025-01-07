import networkx as nx
import time
from branch_and_bound import bnb_tsp
from twice_around_the_tree import approx_tsp_twice_around_the_tree

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

if __name__ == "__main__":
    start = time.time()
    file_name = 'tsp_examples/atest.tsp'
    G = read_tsp_file(file_name)
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
    end = time.time()
    print("Melhor caminho:", solution)
    print("Custo mínimo:", cost)
    print("Tempo de execução:", end - start, "segundos")
    print("Tempo de execução:", (end - start) / 60, "minutos")
    solution, cost = approx_tsp_twice_around_the_tree(G)
    end = time.time()
    print("Melhor caminho:", solution)
    print("Custo mínimo:", cost)
    print("Tempo de execução:", end - start, "segundos")
    print("Tempo de execução:", (end - start) / 60, "minutos")
    
    

