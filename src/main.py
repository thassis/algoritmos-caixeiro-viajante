import networkx as nx
import time
import os
import signal
import gc
from contextlib import contextmanager

from branch_and_bound import bnb_tsp, bfs_tsp
from twice_around_the_tree import twice_around_the_tree_tsp
from christofides import christofides_tsp

def process_file(file_name, algorithm):
    try:
        total_cost = None
        path = None
        start = time.time()
        if algorithm == 'bnb':
            total_cost, path, memory = bnb_tsp(file_name)
        elif algorithm == 'christofides':
            total_cost, path, memory = christofides_tsp(file_name)
        elif algorithm == 'bfs':
            total_cost, path, memory = bfs_tsp(file_name)
        else:
            total_cost, path, memory = twice_around_the_tree_tsp(file_name)
        end = time.time()
    finally:
        gc.collect()
    print(f"Cost: {total_cost}, Time: {end - start}, Memory: {memory} | {memory / 1024 / 1024} MB")
    return total_cost, path, end - start, memory

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
                with time_limit(1800):
                    total_cost, path, exec_time, memory = process_file(file_path, algorithm)
            except TimeoutException:
                total_cost, path, exec_time, memory = "timeout", None, None, None
            
            with open(out_file_path, 'w') as out_file:
                if total_cost == "timeout":
                    out_file.write("timeout\n")
                else:
                    out_file.write(f"Melhor caminho: {total_cost}\n")
                    out_file.write(f"Custo mínimo: {path}\n")
                    out_file.write(f"Tempo de execução: {exec_time} segundos\n")
                    out_file.write(f"Uso de memória: {memory} bytes\n")
