import os

def read_best_path_from_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if "Melhor caminho:" in line:
                    best_path_value = int(line.split(":")[1].strip())
                    return best_path_value
    except FileNotFoundError:
        return None
    except ValueError:
        return None

if __name__ == "__main__":
    main_file = "optimal_solutions.txt"
    output_folder = "out_twice"
    mismatched_count = 0
    total_checked = 0

    with open(main_file, 'r') as file:
        for line in file:
            try:
                name, value = line.split(":")
                name = name.strip()
                list_value = int(value.strip())
                corresponding_filename = f"{output_folder}/{name}.txt"

                best_path_value = read_best_path_from_file(corresponding_filename)

                if best_path_value is not None:
                    total_checked += 1
                    if best_path_value != list_value:
                        mismatched_count += 1
                        print(f"{name}: {best_path_value/list_value}, {best_path_value, list_value}")

            except ValueError:
                print(f"Erro ao processar linha: {line.strip()}")

    print(f"Total de diferenças encontradas: {mismatched_count}")
    print(f"Total de arquivos processados: {total_checked}")
