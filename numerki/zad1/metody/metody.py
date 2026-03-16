from collections.abc import Callable


def horner(x, coeffs, length):
    result = coeffs[0]
    i = 1
    while i < length:
        result = result * x + coeffs[i]
        i += 1
    return result


def bisekcja(func: Callable[[float], float], a: float,
             b: float) -> float:  # func jest potrzebne w falsi a tu zbędne ale żeby program
    # mógł być wywołany w obu metodach to tez dajemu fun
    return (a + b) / 2


def regula_falsi(func: Callable[[float], float], a: float, b: float) -> float:
    return (a * func(b) - b * func(a)) / (func(b) - func(a))


def find_zero(func: Callable[[float], float], a: float, b: float, stop_type: int, stop_value: int,
              method_step_func) -> tuple[float, int]:
    # method_step_func --> albo bisekcja albo reguła falsi
    # stop_type 1 - liczby po przecinku 2 - iteracja
    # stop_valu epsilon - liczba iteracja lub ilosc liczb po przecinku
    is_valid: bool = False
    iteration_count: int = 0
    # Dane do oszacowanie wyniku
    x_i: float = a
    epsilon: float = 1.0

    # Zamienienie stop_value na dokładność np. 0.001
    if stop_type == 1:
        epsilon *= 0.1 ** stop_value
    while not is_valid:
        x_i_prev = x_i
        x_i = method_step_func(func, a, b)
        if stop_type == 1:
            if abs(x_i - x_i_prev) < epsilon:
                is_valid = True
        else:
            if iteration_count == (stop_value - 1):
                is_valid = True
        if func(x_i) == 0:
            is_valid = True
        # Szukamy gdzie iloczyn jest negatywny i ustawiamy nowy przedzia
        if func(a) * func(x_i) < 0:
            b = x_i
        else:
            a = x_i
        iteration_count += 1
    return x_i, iteration_count
