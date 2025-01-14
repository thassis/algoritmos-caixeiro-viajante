import networkx as nx
import time
import os
import signal
from contextlib import contextmanager

from branch_and_bound import bnb_tsp, bfs_tsp
from twice_around_the_tree import approx_tsp_twice_around_the_tree
from christofides import christofides_tsp

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

def process_file(file_name, algorithm):
    G = read_tsp_file(file_name)
    solution = None
    cost = None
    start = time.time()
    if algorithm == 'bnb':
        A = nx.adjacency_matrix(G).toarray()
        n = len(G.nodes)
        solution, cost, memory = bnb_tsp(A, n)
    elif algorithm == 'christofides':
        solution, cost, memory = christofides_tsp(G)
    elif algorithm == 'bfs':
        solution, cost, memory = bfs_tsp(G)
    else:
        solution, cost, memory = approx_tsp_twice_around_the_tree(G)
    end = time.time()
    return solution, cost, end - start, memory

class TimeoutException(Exception):
    pass

def handle_timeout(signum, frame):
    raise TimeoutException

@contextmanager
def time_limit(seconds):
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

if __name__ == "__main__":
    algorithm = 'christofides'  # 'christofides', 'bfs', 'bnb', 'twice'.
    tsp_folder = 'tsp_examples'
    out_folder = f'out_{algorithm}'
    os.makedirs(out_folder, exist_ok=True)

    for file_name in os.listdir(tsp_folder):
        if file_name.endswith('.tsp'):
            file_path = os.path.join(tsp_folder, file_name)
            out_file_path = os.path.join(out_folder, file_name.replace('.tsp', '.txt'))
            print(f"Processando {file_name} com {algorithm}")
            try:
                with time_limit(10):
                    solution, cost, exec_time, memory = process_file(file_path, algorithm)
            except TimeoutException:
                solution, cost, exec_time, memory = "timeout", None, None, None
            
            with open(out_file_path, 'w') as out_file:
                if solution == "timeout":
                    out_file.write("timeout\n")
                else:
                    out_file.write(f"Melhor caminho: {solution}\n")
                    out_file.write(f"Custo mínimo: {cost}\n")
                    out_file.write(f"Tempo de execução: {exec_time} segundos\n")
                    out_file.write(f"Uso de memória: {memory} bytes\n")
