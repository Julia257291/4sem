from ukladanka import get_target_board


def get_target_positions(rows, cols):
    """Tworzy słownik {wartość: (wiersz, kolumna)} dla stanu docelowego."""
    target_board = get_target_board(rows, cols)
    positions = {}
    for r in range(rows):
        for c in range(cols):
            val = target_board[r][c]
            positions[val] = (r, c)
    return positions


def heuristic_manhattan(board, rows, cols, target_positions):
    """Liczy jak daleko pola są od swoich prawidłowych miejsc, suma kroków, aby dotrzeć do celu"""
    score = 0
    for r in range(rows):
        for c in range(cols):
            val = board[r][c]
            if val != 0:  # Zera nie liczymy
                # Pobieramy współrzędne celu ze słownika
                target_r, target_c = target_positions[val]
                # Liczymy różnicę wierszy i kolumn
                score += abs(r - target_r) + abs(c - target_c)
    return score


def heuristic_hamming(board, target_board, rows, columns):
    """Liczy ile pól jest na swoim miejscu"""
    score = 0
    for r in range(rows):
        for c in range(columns):
            val = board[r][c]
            if val != 0 and val != target_board[r][c]:
                score += 1
    return score
