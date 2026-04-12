def find_biggest_row(matrix, column, length):
    max_value = 0.0
    best_row = column
    for row in range(column, length):  # zaczynamy od kolumny przekazanej, żeby nie powtarzać obliczeń
        if abs(matrix[row][column]) > max_value:
            max_value = abs(matrix[row][column])
            best_row = row
    return best_row


def change_rows(matrix, row1, row2):
    if row1 != row2:
        temp = matrix[row1]
        matrix[row1] = matrix[row2]
        matrix[row2] = temp


def eliminate(macierz, wiersz_glowny, obecna_kolumna, liczba_wierszy):
    element_glowny = macierz[wiersz_glowny][obecna_kolumna]

    if abs(element_glowny) > 1e-9:  # Upewniamy się, że nie dzielimy przez zero
        for wiersz_docelowy in range(wiersz_glowny + 1, liczba_wierszy):
            mnoznik = macierz[wiersz_docelowy][obecna_kolumna] / element_glowny
            for kolumna in range(obecna_kolumna, liczba_wierszy + 1):
                macierz[wiersz_docelowy][kolumna] -= mnoznik * macierz[wiersz_glowny][kolumna]


def eliminacja_gaussa(matrix):
    matrix_len = len(matrix)  # Liczba wierszy
    for column in range(matrix_len):
        current_row = column  # Poruszamy się po przekątnej wiec row i column sa takie same
        best_row = find_biggest_row(matrix, current_row, matrix_len)
        change_rows(matrix, current_row, best_row)
        eliminate(matrix, current_row, column, matrix_len)
    return matrix


def backward_substitution(matrix):
    matrix_len = len(matrix)
    x = [0.0] * matrix_len
    status = "OZNACZONY"
    for row in range(matrix_len - 1, -1, -1):
        all_zeros = True
        for col in range(matrix_len):
            if abs(matrix[row][col]) > 1e-9:
                all_zeros = False
        if all_zeros:
            if abs(matrix[row][matrix_len]) > 1e-9:
                status = "SPRZECZNY"
            else:
                if status != "SPRZECZNY":
                    status = "NIEOZNACZONY"
        else:
            if status == "OZNACZONY":
                suma_podstawien = 0.0
                for col in range(row + 1, matrix_len):
                    suma_podstawien += matrix[row][col] * x[col]
                x[row] = (matrix[row][matrix_len] - suma_podstawien) / matrix[row][row]
    return x, status
