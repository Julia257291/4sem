import math as m
FUNCTIONS = {
    "1" : {
        "opis" : "Wielomian: x^4 - x^2 + 3x - 2",

        "f" : lambda x: ((x * x - 1) * x + 3) * x - 2   #Policzenie Hornera
        #TODO: Funckja obliczająca schemat Hornera automatycznie
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
    return FUNCTIONS[choice]

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
    return METHOD[choice]


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
                    print("Błąd: Funkcja na końcach przedziału musi mieć różne znaki!")
            else:
                print("a musi być mniejsze od b!")
        except ValueError:
            print("Błąd: Podaj poprawne liczby")
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
            choice = int(input("Podaj wartość epsilon - dokładność liczb po przecinku").strip())
            if 1 < choice < 8:
                result = choice
                is_valid = True
        else:  #Liczba iteracji, zakładany przedział od 1 do 25
            choice = int(input("Podaj wartość epsilon - ilość iteracji").strip())
            if 1 < choice < 25:
                result = choice
                is_valid = True
    return result

#metoda bisekcji

#reguła falsi

#Oszacowanie dokładności wyniku

#Narysowanie funckji i zapisanie

def main():
    function = get_function()
    method = get_metod()
    f = function["f"]
    interval = get_interval(f) #Tablica 0 - start, 1 - end
    stop_condition = get_stopcondition() # Mamy integer 1-2
    value = get_value(stop_condition)