import math
from metody.metody import horner, bisekcja, regula_falsi

FUNCTIONS = {
    "1": {
        "opis": "Wielomian: x^4 - x^2 + 3x - 2",
        "f": lambda x: horner(x, [1, 0, -1, 3, -2], 5)
    },
    "2": {
        "opis": "Trygonometryczna: 2cos(0.5x) + 1",
        "f": lambda x: 2 * math.cos(0.5 * x) + 1
    },
    "3": {
        "opis": "Wykładnicza: e^x - 2",
        "f": lambda x: math.exp(x) - 2
    },
    "4": {
        "opis": "Złożona: sin(x^2) + 3x - 3",
        "f": lambda x: math.sin(x * x) + 3 * x - 3
    }
}

METHOD = {
    "1": ("Metoda bisekcji", bisekcja),
    "2": ("Reguła Falsi", regula_falsi)
}

STOP_CONDITION = {
    1: "Liczby po przecinku",
    2: "Liczba iteracji"
}
