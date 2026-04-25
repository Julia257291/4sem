MOVES = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (-1, 0),
    'D': (1, 0)
}  # Do zmiany wiersz i kolumn, żeby nie była generowana z każdym wywołanie funkcji


def get_target_board(rows, columns):
    """Generuje układ docelowy dla podanych wymiarów. """
    target = []
    for r in range(rows):
        row = []
        for c in range(columns):
            val = r * columns + c + 1  # Obliczamy dla każdego miejsca
            if val == rows * columns:  # Ostatnie jest 0
                val = 0
            row.append(val)
        target.append(row)

    return tuple(tuple(row) for row in target)


def is_goal(board, rows, columns):
    """ Sprawdza, czy bieżący stan planszy jest równy stanowi docelowemu."""
    return board == get_target_board(rows, columns)


def find_zero(board, rows, cols):
    """Zwracamy współrzędne zera (row, column)"""
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 0:
                return r, c
    return None


def get_neighbors(board, rows, columns, order="LUDR"):
    """Generuje sąsiadów, zwracając układankę sąsiada oraz wykonany ruch."""
    neighbors = []
    zero_row, zero_col = find_zero(board, rows, columns)  # Pozycja zera teraz
    for move in order:
        change_row, change_column = MOVES[move]  # Dostajemy wartości o które będziemy zmieniać
        new_row, new_col = zero_row + change_row, zero_col + change_column
        if 0 <= new_row < rows and 0 <= new_col < columns:
            temp_board = []  # Nie będziemy modyfikować oryginalnej układanki
            for row in range(rows):
                temp_row = []
                for column in range(columns):
                    temp_row.append(board[row][column])
                temp_board.append(temp_row)
            change = temp_board[new_row][new_col]
            temp_board[zero_row][zero_col] = change
            temp_board[new_row][new_col] = 0
            neighbors.append((tuple(tuple(r) for r in temp_board), move))
    return neighbors


def reconstruct_path(came_from, current_state):
    """Zwróci drogę potrzebną do rozwiązania układanki"""
    path = []
    while current_state in came_from:
        parent, move = came_from[current_state]
        if move is None: break  # Dotarliśmy do startu
        path.append(move)
        current_state = parent
    path.reverse()
    return "".join(path)