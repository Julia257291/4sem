import math

def simpson(function, start, finish, nodes):
    step = (finish - start)/ nodes
    odd_nodes = 0.0
    even_nodes = 0.0
    for node in range(1,nodes):
        x = start + node * step #Liczymy wartość dla x
        if node % 2 == 1:
            odd_nodes += function(x)
        if node % 2 == 0:
            even_nodes += function(x)

    return (step/ 3.0) * (function(start) + function(finish) + 4.0 * odd_nodes + 2.0 * even_nodes)


def iterative_simpson(function, start, finish, accuracy):
    nodes = 2 # żeby stworzyły się 3 pkt, które są minimum
    result = simpson(function, start, finish, nodes)
    nodes *= 2 # Zwiększamy podwójnie zgodnie z treścią zadania
    new_result = simpson(function, start, finish, nodes)

    is_finished = False
    while not is_finished:
        if abs(new_result - result) < accuracy:
            is_finished = True
        result = new_result
        nodes *= 2
        new_result = simpson(function, start, finish, nodes)

    return new_result


def limit_on_edges(function, start, finish, accuracy):
    sum = 0.0
    step = 0.5
    a = start
    b = start + finish * step
    is_finished = False
    while not is_finished:
        if finish > 0:
            part_value = iterative_simpson(function, a, b, accuracy)
        else:
            part_value = iterative_simpson(function, b, a, accuracy)
        sum += part_value
        if abs(part_value) < accuracy:
            is_finished = True
        else:
            a = b
            step /= 2.0
            b = a + finish * step
    return sum


def simpson_complete(function, accuracy):
    wagowa_funkcja = lambda  x: function(x) * (1.0/ math.sqrt(1.0 - x * x))
    right_part = limit_on_edges(wagowa_funkcja, 0.0, 1.0, accuracy) # 0,1.0
    left_part = limit_on_edges(wagowa_funkcja, 0.0, -1.0, accuracy) #-1.0, 0
    total = right_part + left_part
    return total

