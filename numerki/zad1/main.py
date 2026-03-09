from UI.ui import get_function, get_value, get_metod, get_interval, get_stopcondition
from metody.metody import find_zero
from wizualizajca.grafy import generate_plot_data, draw_plot
from stałe.funkcje import METHOD
def main():
    f = get_function()
    method = get_metod()
    method_name =METHOD[method][0]
    method_func = METHOD[method][1]
    interval = get_interval(f) #Tablica 0 - start, 1 - end
    stop_condition = get_stopcondition() # Mamy integer 1-2
    epsilon = get_value(stop_condition)
    root1, iters1 = find_zero(f, interval[0], interval[1], stop_condition, epsilon, method_func)
    print(f"Uruchomiono: {method_name}")
    print(f"Wynik: {root1}")
    print(f"Liczba iteracji: {iters1}")

    if method == "1":
        other_method = "2"
    else:
        other_method = "1"

    other_name = METHOD[other_method][0]
    other_func = METHOD[other_method][1]

    root2, iters2 = find_zero(f, interval[0], interval[1], stop_condition, epsilon, other_func)
    print(f"Uruchomiono: {other_name}")
    print(f"Wynik: {root2}")
    print(f"Liczba iteracji: {iters2}")

    x, y = generate_plot_data(f, interval[0], interval[1])
    draw_plot(x, y, roots=[root1, root2])

main()