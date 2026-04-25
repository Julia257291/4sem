from ukladanka import *
from heurystyka import *
import heapq


def astar(initial_board, rows, cols, heuristic="manhattan"):
    s = tuple(tuple(row) for row in initial_board)
    goal_board = get_target_board(rows, cols)
    goal = tuple(tuple(row) for row in goal_board)

    if s == goal:
        return "", 1, 0, 0

    if heuristic == "manhattan":
        target_positions = get_target_positions(rows, cols)


    open_set = []
    tie_breaker = 0

    if heuristic == "manhattan":
        h = heuristic_manhattan(initial_board, rows, cols, target_positions)
    elif heuristic == "hamming":
        h = heuristic_hamming(initial_board, goal_board, rows, cols)

    heapq.heappush(open_set, (h, tie_breaker, 0, s))

    came_from = {s: (None, None)}
    g_score = {s: 0}
    visited = set()

    processed_count = 0
    max_depth = 0

    while open_set:
        f, _, depth, current = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        processed_count += 1
        max_depth = max(max_depth, depth)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, len(g_score), processed_count, depth

        for neighbor_list, move in get_neighbors(current, rows, cols, "LUDR"):
            neighbor = tuple(tuple(row) for row in neighbor_list)

            tentative_g = depth + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g

                if heuristic == "manhattan":
                    h = heuristic_manhattan(neighbor_list, rows, cols, target_positions)
                elif heuristic == "hamming":
                    h = heuristic_hamming(neighbor_list, goal_board, rows, cols)
                else:
                    h = 0

                f_score = tentative_g + h
                tie_breaker += 1

                heapq.heappush(open_set, (f_score, tie_breaker, tentative_g, neighbor))

    return "-1", len(g_score), processed_count, max_depth
