import math as m
FUNCTIONS = {
    "1" : {
        "opis" : "Wielomian: x^4 - x^2 + 3x - 2",
        "f" : lambda x: horner(x, FUNCTIONS["1"]["coeffs"], len(FUNCTIONS["1"]["coeffs"])),
        "coeffs" : [1, 0, -1, 3, -2]
    },
    "2" : {
        "opis" : "Trygonometryczna: 2cos(0.5x) + 1",
        "f" : lambda x : 2* m.cos(0.5 * x) + 1
    },
    "3" : {
        "opis" : "Wykładnicza: e^x - 2",
        "f" : lambda x: m.exp(x) - 2
    },
    "4" : {
        "opis" : "Złożona: sin(x^2) +3x -3",
        "f" : lambda x: m.sin(x**2) + 3*x -3
    }
}

METHOD = {
    "1" : "Metoda bisekcji",
    "2" : "Reguła Falsi"
}

STOP_CONDITION = {
    1 : "Liczby po przecinku",
    2 : "Liczba iteracji"
}