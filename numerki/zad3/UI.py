from functions import FUNCTIONS
def get_function():
    for function in FUNCTIONS:
        print(f"{function}: {FUNCTIONS[function]['opis']}")
    is_valid = False
    user_input = ""
    while not is_valid:
        user_input = input("Wybór: (1-4) ")
        if user_input in FUNCTIONS:
            is_valid = True
        else:
            print("Niepoprawny wybór")
    return FUNCTIONS[user_input] #zwracamy słownik
