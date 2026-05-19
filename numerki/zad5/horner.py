def horner(x: float, coeffs: list[float], length: int) -> float:
    result: float = coeffs[0]
    i: int = 1
    while i < length:
        result = result * x + coeffs[i]
        i += 1
    return result
