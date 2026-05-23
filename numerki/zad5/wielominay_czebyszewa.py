def wielomiany_czebyszewa(degree: int) -> list:
    if degree == 0:
        return [[1.0]]
    T = [] # Tworzymy liste do ktorych bedziemy załączać wielomiany
    T.append([1.0])  # T_0 = 1
    T.append([1.0, 0.0])  # T_1 = x

    i = 2
    # T_k = 2x T_k-1 - T_k-2
    while degree >= i:
        wielomian = [0.0] * (i+1) #tworzymy miejsce

        j = 0
        while j < len(T[i-1]):
            wielomian[j] = 2.0 * T[i-1][j]
            j += 1
        k = 0
        while k < len(T[i - 2]):
            wielomian[k + 2] -= T[i - 2][k]
            k += 1
        i += 1
        T.append(wielomian)
    return T