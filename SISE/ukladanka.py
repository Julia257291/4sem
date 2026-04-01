def get_target_board(rows, columns):
    """Generuje układ docelowy dla podanych wymiarów. """
    target = []
    for r in range(rows):
        row = []
        for c in range(columns):
            val = r * columns + c + 1 #Obliczamy dla każdego miejsca
            if val == rows * columns: #Ostatnie jest 0
                val = 0
            row.append(val)
        target.append(row)

    return target


def is_goal(board, rows, columns):
    """ Sprawdza, czy bieżący stan planszy jest równy stanowi docelowemu."""
    return board == get_target_board(rows, columns)

'''if __name__ == "__main__":
    rows, cols = 4, 4
    target = get_target_board(rows, cols)
    print("Wygenerowany wzorzec:")
    for row in target:
        print(row)
    print("Czy wzorzec to stan docelowy?", is_goal(target, rows, cols))'''