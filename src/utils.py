import networkx as nx
import random

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

def generate_tsp_instance(name, num_points, file_path):
    with open(file_path, "w") as file:
        file.write(f"NAME: {name}\n")
        file.write("TYPE: TSP\n")
        file.write(f"COMMENT: {num_points}-city problem\n")
        file.write(f"DIMENSION: {num_points}\n")
        file.write("EDGE_WEIGHT_TYPE: EUC_2D\n")
        file.write("NODE_COORD_SECTION\n")
        for i in range(num_points):
            x, y = random.randint(1, 1000), random.randint(1, 1000)
            file.write(f"{i} {x} {y}\n")
        file.write("EOF\n")

def generate_tsp_instances(file_path):
    dimensions = [5, 7, 9, 11]
    for i in range(0, 10):
        for instance_number in range(1, 5):
            dimension = dimensions[instance_number - 1]
            filename = f"{file_path}/tsp_instance_{dimension}_{i}.tsp"
            generate_tsp_instance(f"instance_{dimension}", dimension, filename)
