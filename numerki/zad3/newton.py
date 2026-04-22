def evaluate_newton(coefficients, x, x_nodes):
    #W(x) = a0 + a1(x-x0) +a2(x-x0)(x-x1) + a3(x-x0)(x-x1)(x-x2) ...
    length = len(coefficients)
    product = 1.0
    i = 1
    result = coefficients[0]
    while i < length:
        product *= (x - x_nodes[i - 1])
        result += coefficients[i] * product
        i += 1
    return result

def calculate_coefficients(x,y):
    n = len(x)
    coeffs = list(y)
    j = 1
    while j < n:
        k = n - 1
        while k >= j:
            licznik = coeffs[k] - coeffs[k - 1]
            mianownik = x[k] - x[k - j]
            coeffs[k] = licznik / mianownik
            k -= 1
        j += 1
    return coeffs