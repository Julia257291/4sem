from math import pi, cos

def gauss_chebyshev(function, n):
    total_sum = 0.0
    weight = pi / n
    for i in range(1, n + 1):
        x_i = cos((2.0 * i - 1.0) * pi / (2.0 * n))
        total_sum += function(x_i)

    return weight * total_sum