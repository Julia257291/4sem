from collections.abc import Callable

from stałe.funkcje import FUNCTIONS, METHOD, STOP_CONDITION


def get_function() -> Callable[[float], float]:
    is_valid: bool = False
    choice: str = ""
    while not is_valid:
        print("1. Wielomian: x^4 - x^2 + 3x - 2")
        print("2. Trygonometryczna: 2cos(0.5x) + 1")
        print("3. Wykładnicza: e^x - 2")
        print("4. Złożona: sin(x^2) + 3x - 3")
        choice = input("Wybór funckji 1-4: ").rstrip()
        if choice in FUNCTIONS:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return FUNCTIONS[choice]["f"]


def get_method() -> str:
    choice: str = ""
    is_valid: bool = False
    while not is_valid:
        print("Metody: ")
        print("1. Metoda bisekcji")
        print("2. Reguła Falsi")
        choice = input("Wybierz metodę 1-2: ").rstrip()
        if choice in METHOD:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return choice


def get_interval(f: Callable[[float], float]) -> list[float]:
    a: float = 0.0
    b: float = 0.0
    is_valid: bool = False
    while not is_valid:
        try:
            temp_a = float(input("Podaj wartość a (lewy kraniec):  ").rstrip())
            temp_b = float(input("Podaj wartość b (prawy kraniec): ").rstrip())
            if temp_a < temp_b:
                if f(temp_a) * f(temp_b) < 0:
                    a = temp_a
                    b = temp_b
                    is_valid = True
                else:
                    print("Funkcja na końcach przedziału musi mieć różne znaki!")
            else:
                print("a musi być mniejsze od b")
        except ValueError:
            print("Podaj poprawne liczby")
    return [a, b]


def get_stopcondition() -> int:
    choice: int = 0
    is_valid: bool = False
    while not is_valid:
        print("Wybierz kryterium zatrzymania: ")
        print("1. Dokładność do ilości liczb po przecinku")
        print("2. Liczba iteracji")
        choice = int(input("Wybór 1-2: ").rstrip())
        if choice in STOP_CONDITION:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return choice


def get_value(stop) -> int:
    result: int = 0
    is_valid: bool = False
    while not is_valid:
        if stop == 1:  # Dokładność liczb po przecinku, zakładany przedział od 1 do 18
            try:
                choice = int(input("Podaj wartość epsilon dokładność liczb po przecinku: ").rstrip())
                if 1 <= choice < 18:
                    result = choice
                    is_valid = True
                else:
                    raise ValueError
            except ValueError:
                print("Niepoprawne")
        else:  # Liczba iteracji
            try:
                choice = int(input("Podaj wartość epsilon (ilość iteracji): ").rstrip())
                if 1 < choice:
                    result = choice
                    is_valid = True
                else:
                    raise ValueError
            except ValueError:
                print("Niepoprawne")
    return result
