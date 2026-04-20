"""
AUTORZY:
Patryk Gołacki 257275
Julia Szcześniak 257291

20.04.26
"""

from gauss_elimination import *
from matrix_load import load_matrix_from_file


def main():
    numerek = input("Podaj nazwe pliku z macierza: A-J ")
    path = f"text_files/{numerek}.txt"
    matrix = load_matrix_from_file(path) #from matrix_load.py
    if not matrix:
        print("Nie udalo sie wczytac macierzy lub plik jest pusty.")
        return

    matrix_length = len(matrix)  # Liczba wierszy
    # Sprawdzenie, czy macierz ma poprawne wymiary n x (n+1)
    for row in matrix:
        if len(row) != matrix_length + 1:  # Kolumna więcej przez wyniki
            print("Nieprawidlowe wymiary macierzy w pliku.")
            return

    #Tworzenie macierzy trójkątnej górnej:
    triangular_matrix = eliminacja_gaussa(matrix)
    #podstawienie w tył
    result, status = backward_substitution(triangular_matrix)

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
