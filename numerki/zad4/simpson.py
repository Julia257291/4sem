import math

def simpson(function, start: float, finish: float, nodes: int) -> float:
    step: float = (finish - start)/ nodes
    odd_nodes: float = 0.0
    even_nodes: float = 0.0
    for node in range(1,nodes):
        x = start + node * step #Liczymy wartość dla x
        if node % 2 == 1:
            odd_nodes += function(x)
        if node % 2 == 0:
            even_nodes += function(x)

    return (step/ 3.0) * (function(start) + function(finish) + 4.0 * odd_nodes + 2.0 * even_nodes)


def iterative_simpson(function, start: float, finish: float, accuracy: float) -> float:
    nodes: int = 2 # żeby stworzyły się 3 pkt, które są minimum
    result: float = simpson(function, start, finish, nodes)
    nodes *= 2 # Zwiększamy podwójnie zgodnie z treścią zadania
    new_result: float = simpson(function, start, finish, nodes)

    is_finished: bool = False
    while not is_finished:
        if abs(new_result - result) < accuracy:
            is_finished = True
        result = new_result
        nodes *= 2
        new_result = simpson(function, start, finish, nodes)

    return new_result


def limit_on_edges(function, start: float, finish: float, accuracy: float) -> float:
    sum: float = 0.0
    step: float = 0.5
    a: float = start
    b: float = start + finish * step
    is_finished: bool = False
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


def simpson_complete(function, accuracy:float) ->float:
    wagowa_funkcja = lambda  x: function(x) * (1.0/ math.sqrt(1.0 - x * x))
    right_part: float = limit_on_edges(wagowa_funkcja, 0.0, 1.0, accuracy) # 0,1.0
    left_part: float = limit_on_edges(wagowa_funkcja, 0.0, -1.0, accuracy) #-1.0, 0
    total: float = right_part + left_part
    return total

