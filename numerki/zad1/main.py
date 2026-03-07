FUNCTIONS = {
    "1" : {
        "opis" : "Wielomian: x^4 - x^2 + 3x - 2",
        "f" : "funckja"
    },
    "2" : {
        "opis" : "Trygonometryczna: 2cos(0.5x) + 1",
        "f" : "funkcja"
    },
    "3" : {
        "opis" : "Wykładnicza: 3^x - 2",
        "f" : "funkcja"
    },
    "4" : {
        "opis" : "Złożona: sin(x^2) +3x -3",
        "f" : "funckja"
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
    while True:
        print("1. Wielomian: x^4 - x^2 + 3x - 2")
        print("2. Trygonometryczna: 2cos(0.5x) + 1")
        print("3. Wykładnicza: 3^x - 2")
        print("4. Złożona: sin(x^2) +3x -3")

        choice = input("Wybór funckji 1-4: ")

        if choice in FUNCTIONS:
            return FUNCTIONS[choice]
        else:
            print("Nieprawidłowy wybór")


def get_metod():
    while True:
        print("Metody: ")
        print("1. Metoda bisekcji")
        print("2. Reguła Falsi")
        choice = input("Wybierz metodę 1-2: ")
        if choice in METHOD:
            return METHOD[choice]
        else:
            print("Nieprawidłowy wybór")


def get_interval(f):  # Dodajemy f jako parametr
    while True:
        try:
            a = float(input("a: ").strip())
            b = float(input("b: ").strip())
            if a >= b:
                print("a musi być mniejsze od b!")
                continue

            # To jest kluczowy warunek z zadania (Warunek Bolzano)
            if f(a) * f(b) < 0:
                return [a, b]
            else:
                print("Błąd: Funkcja na końcach przedziału musi mieć różne znaki!")
        except ValueError:
            print("Podaj poprawne liczby!")

def get_stopcondition():
    while True:
        print("Wybierz kryterium zatrzymania: ")
        print("1. Dokładność do ilości liczb po przecinku")
        print("2. Liczba iteracji")
        choice = int(input("Wybór 1-2: "))
        if choice in STOP_CONDITION:
            return choice #Oddaje numer wyboru
        else:
            print("Nieprawidłowy wybór")

def get_value(stop):
    while True:
        if stop == 1: #Dokładność liczb po przecinku, zakładany przedział od 1 do 8
            choice = int(input("Podaj wartość epsilon - dokładność liczb po przecinku").strip())
            if 1 < choice < 8:
                return choice
        else:  #Liczba iteracji, zakładany przedział od 1 do 25
            choice = int(input("Podaj wartość epsilon - ilość iteracji").strip())
            if 1 < choice < 25:
                return choice

#metoda bisekcji

#reguła falsi

#Oszacowanie dokładności wyniku

#Narysowanie funckji i zapisanie

#Horner dla wielomianu

def main():
    function = get_function()
    method = get_metod()
    f = function["f"]
    interval = get_interval(f) #Tablica 0 - start, 1 - end
    stop_condition = get_stopcondition() # Mamy integer 1-2
    value = get_value(stop_condition)
