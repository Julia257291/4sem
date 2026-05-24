import matplotlib.pyplot as plt
import math
from horner import horner
from aproksymacja import aproksymacja

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
    },
    "5": {
        "opis": "Wartość bezwględna: |x| + 3 - |x^2|",
        "f": lambda x: math.fabs(x) + 3 - math.fabs(x*x)
    }
}

def main():
    is_function = False
    while not is_function:
        for key in FUNCTIONS:
            print(f"{key}. {FUNCTIONS[key]["opis"]}")
        user_func = input("Proszę wybrać funkcję: 1-5 ")
        if user_func in FUNCTIONS:
            is_function = True
    function = FUNCTIONS[user_func]["f"]
    is_interval = False
    a, b = 0.0, 0.0
    while not is_interval:
        a = float(input("Podaj początek przedziału: "))
        b = float(input("Podaj koniec przedziału: "))
        if a < b:
            is_interval = True
        else:
            print("Niepoprawny przedział")
    is_nodes = False
    while not is_nodes:
        nodes_num = int(input("Podaj ilość węzłów: "))
        if nodes_num > 0:
            is_nodes = True
    f_mapped = lambda x: function(((b - a) * x + (a + b)) / 2.0)
    is_mode = False
    mode = 0
    while not is_mode:
        print("Wybierz tryb pracy programu:")
        print("1. Podaj stopień wielomianu")
        print("2. Podaj oczekiwany błąd")
        mode = int(input("Wybór: "))
        if mode == 1 or mode == 2:
            is_mode = True
        else:
            print("Niepoprawny wybór")
    score = []
    points_x = []
    points_y = []
    error = 0.0
    if mode == 1:
        degree = int(input("Podaj stopień wielomianu aproksymującego: "))
        score, points_x, points_y, error = aproksymacja(f_mapped, degree, nodes_num)
        print(f"Maksymalny błąd aproksymacji wynosi: {error}")
    else:
        accuracy = float(input("Podaj oczekiwany maksymalny błąd: "))
        degree = 1
        max_degree = 20
        is_finised = False

        while not is_finised and degree <= max_degree:
            score, points_x, points_y, error = aproksymacja(f_mapped, degree, nodes_num)
            if error <= accuracy:
                is_finised = True
                print(f"Wymagana dokładność osiągnięta dla wielomianu stopnia: {degree}")
                print(f"Maksymalny błąd aproksymacji wynosi: {error}")
            else:

                degree += 1
        if not is_finised:
            print("Nie ma rozwiązania")

    #Rysowanie grafu
    real_x = []
    real_y = []
    i = 0
    while i < len(points_x):
        t = ((b - a) * points_x[i] + (a + b)) / 2.0
        real_x.append(t)
        real_y.append(function(t))
        i += 1
    plt.figure(figsize=(10, 6))
    plt.plot(real_x, real_y, label="Funkcja oryginalna", color="blue", linewidth=2)
    plt.plot(real_x, points_y, label=f"Aproksymacja (stopień {degree})", color="red", linestyle="--")
    plt.title("Aproksymacja średniokwadratowa wielomianami Czebyszewa")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
