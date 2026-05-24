from math import pi, cos

def gauss_czebyszew(function, n: int) -> float:
    total_sum: float = 0.0
    weight: float = pi / n
    for i in range(1, n + 1):
        x_i: float = cos((2.0 * i - 1.0) * pi / (2.0 * n))
        total_sum += function(x_i)

    return weight * total_sum