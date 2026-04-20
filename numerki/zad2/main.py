"""
AUTORZY:
Patryk Gołacki 257275
Julia Szcześniak 257291

20.04.26
"""

from gauss_elimination import *
from matrix_load import load_matrix_from_file


def main() -> None:
    numerek: str = input("Podaj nazwe pliku z macierza: A-J ")
    path: str = f"text_files/{numerek}.txt"

    # Próba wczytania macierzy
    matrix: list[list[float]] = load_matrix_from_file(path)  # from matrix_load.py

    if not matrix:
        print("Nie udalo sie wczytac macierzy lub plik jest pusty.")
        return

    matrix_length: int = len(matrix)  # Liczba wierszy

    # Sprawdzenie, czy macierz ma poprawne wymiary n x (n+1)
    for row in matrix:
        if len(row) != matrix_length + 1:  # Kolumna więcej przez wyniki
            print("Nieprawidlowe wymiary macierzy w pliku.")
            return

    # Tworzenie macierzy trójkątnej górnej:
    triangular_matrix: list[list[float]] = eliminacja_gaussa(matrix)

    # Podstawienie w tył - rozpakowanie wyniku do zmiennych z typami
    result: list[float]
    status: str
    result, status = backward_substitution(triangular_matrix)

    # Logika wyświetlania wyników
    if status == "OZNACZONY":
        print("Uklad jest oznaczony. Rozwiazania:")
        for i in range(matrix_length):
            print(f"x_{i + 1} = {result[i]:.4f}")
    elif status == "NIEOZNACZONY":
        print("Uklad jest nieoznaczony.")
    elif status == "SPRZECZNY":
        print("Uklad jest sprzeczny - brak rozwiazan.")


if __name__ == "__main__":
    main()
