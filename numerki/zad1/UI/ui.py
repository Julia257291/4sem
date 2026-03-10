from stałe.funkcje import FUNCTIONS, METHOD, STOP_CONDITION
def get_function():
    is_valid = False
    choice = ""
    while not is_valid:
        print("1. Wielomian: x^4 - x^2 + 3x - 2")
        print("2. Trygonometryczna: 2cos(0.5x) + 1")
        print("3. Wykładnicza: e^x - 2")
        print("4. Złożona: sin(x^2) +3x -3")
        choice = input("Wybór funckji 1-4: ")
        if choice in FUNCTIONS:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return FUNCTIONS[choice]["f"]

def get_metod():
    choice = ""
    is_valid = False
    while not is_valid:
        print("Metody: ")
        print("1. Metoda bisekcji")
        print("2. Reguła Falsi")
        choice = input("Wybierz metodę 1-2: ")
        if choice in METHOD:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return choice


def get_interval(f):
    a = 0.0
    b = 0.0
    is_valid = False
    while not is_valid:
        try:
            # Pobieramy dane jako float
            temp_a = float(input("a: ").strip())
            temp_b = float(input("b: ").strip())
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

def get_stopcondition():
    choice = ""
    is_valid = False
    while not is_valid:
        print("Wybierz kryterium zatrzymania: ")
        print("1. Dokładność do ilości liczb po przecinku")
        print("2. Liczba iteracji")
        choice = int(input("Wybór 1-2: "))
        if choice in STOP_CONDITION:
            is_valid = True
        else:
            print("Nieprawidłowy wybór")
    return choice

def get_value(stop):
    result = 0
    is_valid = False
    while not is_valid:
        if stop == 1: #Dokładność liczb po przecinku, zakładany przedział od 1 do 8
            try:
                choice = int(input("Podaj wartość epsilon dokładność liczb po przecinku").strip())
                if 1 < choice < 18:
                    result = choice
                    is_valid = True
            except ValueError:
                print("Niepoprawne")
        else:  #Liczba iteracji, zakładany przedział od 1 do 25
            try:
                choice = int(input("Podaj wartość epsilon ilość iteracji").strip())
                if 1 < choice < 50:
                    result = choice
                    is_valid = True
            except ValueError:
                print("Niepoprawne")
    return result