def find_biggest_row(matrix: list[list[float]], column: int, length: int) -> int:
    max_value: float = 0.0
    best_row: int = column  # bo idziemy po przekątnej więc to samo
    for row in range(column, length):  # zaczynamy od kolumny przekazanej
        if abs(matrix[row][column]) > max_value:  # Sprawdzamy wartości w tej kolumnie w innych rzędach
            max_value = abs(matrix[row][column])
            best_row = row
    return best_row


def change_rows(matrix: list[list[float]], row1: int, row2: int) -> None:
    if row1 != row2:
        temp = matrix[row1]
        matrix[row1] = matrix[row2]
        matrix[row2] = temp


def eliminate(matrix: list[list[float]], main_row: int, current_column: int, num_rows: int) -> None:
    main_element: float = matrix[main_row][current_column]  # element główny którym będziemy eliminiować

    if abs(main_element) > 1e-9:  # Upewniamy się, że nie dzielimy przez zero
        for target_row in range(main_row + 1, num_rows):
            coefficient = matrix[target_row][current_column] / main_element  # mnożnik
            for column in range(current_column, num_rows + 1):
                matrix[target_row][column] -= coefficient * matrix[main_row][column]


def eliminacja_gaussa(matrix: list[list[float]]) -> list[list[float]]:
    matrix_len: int = len(matrix)  # Liczba wierszy
    for column in range(matrix_len):
        current_row: int = column  # Poruszamy się po przekątnej wiec row i column sa takie same
        best_row: int = find_biggest_row(matrix, current_row, matrix_len)
        change_rows(matrix, current_row, best_row)
        eliminate(matrix, current_row, column, matrix_len)
    return matrix


def backward_substitution(matrix: list[list[float]]) -> tuple[list[float], str]:
    matrix_len: int = len(matrix)
    x: list[float] = [0.0] * matrix_len
    status: str = "OZNACZONY"
    for row in range(matrix_len - 1, -1, -1):  # Od samego dołu
        all_zeros: bool = True
        for col in range(matrix_len):  # Sprawdzamy czy w ostatnim rzędzie są same zera
            if abs(matrix[row][col]) > 1e-9:
                all_zeros = False
        if all_zeros:
            if abs(matrix[row][matrix_len]) > 1e-9:  # Sprzawdzamy czy np. 0 = 5
                status = "SPRZECZNY"
            else:
                status = "NIEOZNACZONY"
        else:
            if status == "OZNACZONY":
                suma_podstawien: float = 0.0
                for col in range(row + 1, matrix_len):
                    suma_podstawien += matrix[row][col] * x[col]
                x[row] = (matrix[row][matrix_len] - suma_podstawien) / matrix[row][row]
    return x, status
