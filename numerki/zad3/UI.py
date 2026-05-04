from functions import FUNCTIONS, FunctionData


def get_function() -> FunctionData:
    for function_key in FUNCTIONS:
        print(f"{function_key}: {FUNCTIONS[function_key]['opis']}")

    is_valid: bool = False
    user_input: str = ""

    while not is_valid:
        user_input = input("Wybór: (1-5) ")
        if user_input in FUNCTIONS:
            is_valid = True
        else:
            print("Niepoprawny wybór")

    return FUNCTIONS[user_input]
