from horner import *
from simpson import *
from czebyszew import *
import math

FUNKCJE = {
    "1": {
        "opis": "f(x) = 2x + 1",
        "coeffs": [2.0, 1.0]
    },
    "2": {
        "opis": "f(x) = 2x^3 - x^2 + 3x - 1",
        "coeffs": [2.0, -1.0, 3.0, -1.0]
    },
    "3": {
        "opis": "f(x) = sin(x) + 2",
        "func": lambda x: math.sin(x)
    },
    "4": {
        "opis": "f(x) = e^x",
        "func": lambda x: math.exp(x)
    }
}

def main():
    for funkcja in FUNKCJE:
        print(f"{funkcja}. {FUNKCJE[funkcja]['opis']}")
    is_correct = False
    while not is_correct:
        choice = input("Wybierz numer: ")
        if choice in FUNKCJE:
            is_correct = True
        else:
            print("Nie ma takiej opcji!")
    num = int(choice)
    if num == 1 or num == 2:
        polynomial_coeffs = FUNKCJE[choice]["coeffs"]
        length = len(polynomial_coeffs)
        function = lambda x: horner(x, polynomial_coeffs, length)
    else:
        function = FUNKCJE[choice]["func"]
    is_valid = False
    while not is_valid:
        user_input = input("Proszę podać dokładność np. 0.0001: ")
        accuracy = float(user_input)
        if accuracy > 0:
            is_valid = True
        else:
            print("Dokładność musi być liczbą dodatnią!")
    simpson_result = simpson_complete(function, accuracy)

    nodes_counts = [2, 3, 4, 5]
    for n in nodes_counts:
        score = gauss_czebyszew(function, n)
        print(f"Wynik dla {n} węzłów: {score}")

    # Wyświetlenie wyników
    print(f"Wynik Simpsona {accuracy}: {simpson_result}")



if __name__ == "__main__":
    main()
