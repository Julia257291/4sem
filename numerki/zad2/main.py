"""
AUTORZY:
Patryk Gołacki 257275
Julia Szcześniak 257291

11.04.26
"""

from gauss_elimination import *
from matrix_load import load_matrix_from_file


def main():
    numerek = input("Podaj nazwe pliku z macierza: A-I ")
    path = f"text_files/{numerek}.txt"
    matrix = load_matrix_from_file(path)
    if not matrix:
        print("Nie udalo sie wczytac macierzy lub plik jest pusty.")
        return

    matrix_length = len(matrix)  # Liczba wierszy
    # Sprawdzenie, czy macierz ma poprawne wymiary N x (N+1)
    for row in matrix:
        if len(row) != matrix_length + 1:  # Kolumna więcej przez wyniki
            print("Nieprawidlowe wymiary macierzy w pliku.")
            return

    triangular_matrix = eliminacja_gaussa(matrix)
    result, status = backward_substitution(triangular_matrix)

    if status == "OZNACZONY":
        print("Uklad jest OZNACZONY. Rozwiazania:")
        for i in range(matrix_length):
            print(f"x_{i + 1} = {result[i]:.4f}")
    elif status == "NIEOZNACZONY":
        print("Uklad jest NIEOZNACZONY (posiada nieskonczenie wiele rozwiazan).")
    elif status == "SPRZECZNY":
        print("Uklad jest SPRZECZNY (brak rozwiazan).")


if __name__ == "__main__":
    main()
