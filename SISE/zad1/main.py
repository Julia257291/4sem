import sys
import time
from bfs import *
from dfs import *
from astar import *


def main():
    if len(sys.argv) != 6:
        print("Użycie: python main.py <strategia> <parametr> <plik_we> <plik_wy_sol> <plik_wy_stats>")
        sys.exit(1)

    strategy = sys.argv[1]
    param = sys.argv[2]
    input_file = sys.argv[3]
    sol_file = sys.argv[4]
    stats_file = sys.argv[5]

    board_data = load_board_from_file(input_file)
    if not board_data:
        print(f"Błąd odczytu pliku: {input_file}")
        sys.exit(1)

    rows, cols, initial_board = board_data

    path, visited_count, processed_count, max_depth = "-1", 0, 0, 0

    start_time = time.perf_counter()

    if strategy == "bfs":
        path, visited_count, processed_count, max_depth = bfs(initial_board, rows, cols, order=param)

    elif strategy == "dfs":
        path, visited_count, processed_count, max_depth = dfs(initial_board, rows, cols, order=param)

    elif strategy == "astr":
        heuristic_map = {"manh": "manhattan", "hamm": "hamming"}
        mapped_heuristic = heuristic_map.get(param, "manhattan")
        path, visited_count, processed_count, max_depth = astar(initial_board, rows, cols, heuristic=mapped_heuristic)

    else:
        print(f"Błąd: Nieznana strategia '{strategy}'")
        sys.exit(1)

    end_time = time.perf_counter()

    time_elapsed_ms = round((end_time - start_time) * 1000, 3)

    with open(sol_file, 'w') as f_sol:
        if path == "-1":
            f_sol.write("-1\n")
        else:
            f_sol.write(f"{len(path)}\n")
            f_sol.write(f"{path}\n")

    with open(stats_file, 'w') as f_stats:
        path_len = len(path) if path != "-1" else -1
        f_stats.write(f"{path_len}\n")
        f_stats.write(f"{visited_count}\n")
        f_stats.write(f"{processed_count}\n")
        f_stats.write(f"{max_depth}\n")
        f_stats.write(f"{time_elapsed_ms}\n")


def load_board_from_file(filename):
    with open(filename, 'r') as f:
        # Odczytujemy pierwszą linię z wymiarami
        line = f.readline().split()
        if not line:
            return None

        rows = int(line[0])
        cols = int(line[1])

        # Odczytujemy pozostałe wiersze planszy
        board = []
        for _ in range(rows):
            row_data = list(map(int, f.readline().split()))
            board.append(row_data)

    return rows, cols, board


if __name__ == "__main__":
    main()
