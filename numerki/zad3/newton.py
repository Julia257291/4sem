def evaluate_newton(coefficients: list[float], x: float, x_nodes: list[float]) -> float:
    # W(x) = a0 + a1(x-x0) + a2(x-x0)(x-x1) + a3(x-x0)(x-x1)(x-x2) ...
    length: int = len(coefficients)
    product: float = 1.0
    i: int = 1
    result: float = coefficients[0]

    while i < length:
        product *= (x - x_nodes[i - 1])
        result += coefficients[i] * product
        i += 1

    return result


def calculate_coefficients(x: list[float], y: list[float]) -> list[float]:
    n: int = len(x)
    coeffs: list[float] = list(y)
    j: int = 1

    while j < n:
        k: int = n - 1
        while k >= j:
            licznik: float = coeffs[k] - coeffs[k - 1]
            mianownik: float = x[k] - x[k - j]
            coeffs[k] = licznik / mianownik
            k -= 1
        j += 1

    return coeffs
