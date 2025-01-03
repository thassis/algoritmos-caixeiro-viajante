import networkx as nx

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
            if i < j:
                # nint( sqrt( xd*xd + yd*yd) );
                distance = int((((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2) ** 0.5) + 0.5)
                G.add_edge(i, j, weight=distance)

    return G

if __name__ == "__main__":
    graph = read_tsp_file('tsp_examples/atest.tsp')
    print("Graph constructed with nodes:", graph.nodes())
    print("Graph constructed with edges:", graph.edges(data=True))