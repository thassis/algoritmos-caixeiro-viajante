import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import Polynomial

def create_csv_file(input_folder, algorithm):
    data_summary = []
    optimal_solutions = read_optimal_solutions()

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'): 
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines[0].startswith('NA'):
                    continue
                    # data_summary.append((filename, algorithm, 'NA', '1800', 'NA', 'NA'))
                else:
                    optimal = optimal_solutions[filename.split('.')[0]]
                    
                    #saida foi gerada trocada, best_path é o custo e min_cost é o caminho
                    best_path = lines[1].split(':')[1].strip()
                    min_cost = lines[0].split(':')[1].strip()
                    execution_time = lines[2].split(':')[1].strip().split()[0]
                    memory_usage = lines[3].split(':')[1].strip().split()[0]
                    aproximation = float(min_cost) / optimal
                    data_summary.append((filename, algorithm, min_cost, execution_time, memory_usage, aproximation))

    header = ['Arquivo', 'Algoritmo', 'Custo Mínimo', 'Tempo de Execução (s)', 'Uso de Memória (bytes)', 'Aproximação']

    with open(f'out_{algorithm}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(data_summary)
    return data_summary

def read_optimal_solutions():
    data_dict = {}
    with open('optimal_solutions.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(' : ')
            data_dict[key] = float(value)
    return data_dict

def generate_imgs():
    out_folder = 'images'
    data = pd.read_csv('out.csv')

    data['Pontos'] = data['Arquivo'].str.extract(r'(\d+)').astype(int)

    def plot_with_trendline(x, y, degree=3):
        p = Polynomial.fit(x, y, degree)
        x_new = np.linspace(min(x), max(x), 500)
        y_new = p(x_new)
        return x_new, y_new

    plt.figure(figsize=(10, 6))
    for algo in data['Algoritmo'].unique():
        subset = data[data['Algoritmo'] == algo]
        plt.scatter(subset['Pontos'], subset['Uso de Memória (bytes)'], label=f'{algo} - Data', alpha=0.6)
        x, y = plot_with_trendline(subset['Pontos'], subset['Uso de Memória (bytes)'])
        plt.plot(x, y, label=f'{algo} - Trendline')

    plt.title('Memory Usage by Algorithm (Bytes)')
    plt.xlabel('Number of Points')
    plt.ylabel('Memory Usage (Bytes)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{out_folder}/memory_usage_comparison.png')

    plt.figure(figsize=(10, 6))
    for algo in data['Algoritmo'].unique():
        subset = data[data['Algoritmo'] == algo]
        plt.scatter(subset['Pontos'], subset['Tempo de Execução (s)'], label=f'{algo} - Data', alpha=0.6)
        x, y = plot_with_trendline(subset['Pontos'], subset['Tempo de Execução (s)'])
        plt.plot(x, y, label=f'{algo} - Trendline')

    plt.title('Execution Time by Algorithm (Seconds)')
    plt.xlabel('Number of Points')
    plt.ylabel('Execution Time (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{out_folder}/execution_time_comparison.png')

    plt.figure(figsize=(10, 6))
    for algo in data['Algoritmo'].unique():
        subset = data[data['Algoritmo'] == algo]
        plt.scatter(subset['Pontos'], subset['Aproximação'], label=f'{algo} - Data', alpha=0.6)
        x, y = plot_with_trendline(subset['Pontos'], subset['Aproximação'])
        plt.plot(x, y, label=f'{algo} - Trendline')

    plt.title('Approximation Ratio by Algorithm')
    plt.xlabel('Number of Points')
    plt.ylabel('Approximation Ratio')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{out_folder}/approximation_comparison.png')

if __name__ == "__main__":
    output_folder = "out_twice"
    data_t = create_csv_file(output_folder, 'twice')
    
    output_folder = "out_christofides"
    data_c = create_csv_file(output_folder, 'christofides')
    
    output_file = 'out.csv'
    header = 'Arquivo,Algoritmo,Custo Mínimo,Tempo de Execução (s),Uso de Memória (bytes),Aproximação\n'
    with open(output_file, 'w') as f_out:
        f_out.write(header)
        for row in data_t + data_c:
            f_out.write(','.join(map(str, row)) + '\n')

    generate_imgs()