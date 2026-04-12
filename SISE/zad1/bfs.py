from collections import deque
from ukladanka import *

def bfs(initial_board, rows, cols, order="LUDR"):
    s = tuple(tuple(row) for row in initial_board) #Zmieniamy na tuple
    goal = get_target_board(rows, cols)
    if s == goal:
        return "", 1, 0, 0  # path, odwiedzone, przetworzone, głębokość
    # Q = queue(), visited = set()
    Q = deque([(s, 0)])  # Przechowujemy (stan, głębokość)
    visited = {s}  # Nasze T
    came_from = {s: (None, None)}  # Do sprawdzania Q.has(n) i ścieżki
    # Statystyki
    processed_count = 0
    max_depth = 0

    while Q:
        v, depth = Q.popleft()
        processed_count += 1
        max_depth = max(max_depth, depth)
        for neighbour, move in get_neighbors(v, rows, cols, order):
            if neighbour not in visited:  #Sprawdzamy czy ukladanka byla juz odwiedzona
                if neighbour == goal:
                    came_from[neighbour] = v, move
                    path = reconstruct_path(came_from, neighbour) #Odbudowujemy drogę
                    return path, len(visited) + 1, processed_count, depth + 1
                visited.add(neighbour) #Dodajemy sąsiada do odwiedzonych
                came_from[neighbour] = v, move # Dodajemy do listy skąd przyszliśmy
                Q.append((neighbour, depth + 1))
    return "-1", 0, 0, 0