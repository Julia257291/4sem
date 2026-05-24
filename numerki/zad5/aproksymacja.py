from wielomiany_czebyszewa import *
from horner import *
from zad5.gauss_czebyszew import gauss_czebyszew
from math import pi


def aproksymacja(f_mapped, degree, nodes) -> list:
    wielomiany = wielomiany_czebyszewa(degree)
    A = [0.0] * (degree + 1)
    k = 0
    while k <= degree:
        wielomian_tk = wielomiany[k]
        integrand = lambda x, T_k=wielomian_tk: f_mapped(x) * horner(x, T_k, len(T_k))
        calka = gauss_czebyszew(integrand, nodes)
        if k == 0:
            A[k] = (1.0 / pi) * calka
        else:
            A[k] = (2.0 / pi) * calka
        k += 1
    points_x = []
    points_y = []
    max_error = 0.
    i = -1
    while i <= 1:
        sum = 0.0
        j = 0
        while j <= degree:
            sum += A[j] * horner(i, wielomiany[j], len(wielomiany[j]))
            j += 1
        points_x.append(i)
        points_y.append(sum)
        difference = abs(f_mapped(i) - sum)
        # Jeśli obecna różnica jest większa niż dotychczasowy max_error, zapisujemy ją
        if difference > max_error:
            max_error = difference
        i += 0.01
    return A, points_x, points_y, max_error #Zwracamy też punkty żeby rysować wykres
