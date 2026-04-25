from ukladanka import *


def dfs(initial_board, rows, cols, order="LUDR"):
    s = tuple(tuple(row) for row in initial_board)
    goal = get_target_board(rows, cols)
    if s == goal:
        return "", 1, 0, 0
    stack = [(s, 0)]
    T = set()  # Stany zamknięte
    in_stack = {s: (None, None)}  # Odpowiednik ~S.has(n) i historia

    processed_count = 0
    max_depth = 0
    visited_count = 1

    while stack:
        v, depth = stack.pop()  # Ściągamy z GÓRY (LIFO)
        processed_count += 1
        max_depth = max(max_depth, depth)
        T.add(v)  # Dodajemy do zamkniętych
        if depth < 20:
            # Odwracamy sąsiadów, żeby pierwszy ruch z order był na szczycie stosu
            for n, move in reversed(get_neighbors(v, rows, cols, order)):
                if n not in T and n not in in_stack:
                    visited_count += 1
                    in_stack[n] = (v, move)
                    if n == goal:
                        path = reconstruct_path(in_stack, n)
                        return path, visited_count, processed_count, depth + 1
                    stack.append((n, depth + 1))
    return "-1", visited_count, processed_count, max_depth
