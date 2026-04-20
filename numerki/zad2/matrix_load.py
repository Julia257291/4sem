def load_matrix_from_file(filename: str) -> list[list[float]]:
    matrix: list[list[float]] = []

    with open(filename, 'r') as f:  # otwieramy plik w read mode
        for line in f:
            row: list[float] = []
            parts: list[str] = line.split()  # Rozłączamy części pliku na osobne wyrazy

            for part in parts:
                row.append(float(part))

            matrix.append(row)

    return matrix  # Mamy postać [['1','2','3'],['4','5','6']]
