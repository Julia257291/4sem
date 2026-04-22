def horner(x, coeffs, length):
    result = coeffs[0]
    i = 1
    while i < length:
        result = result * x + coeffs[i]
        i += 1
    return result