from UI import get_function
from newton import *
from graph import draw
from load_nodes import load_nodes

def main():
    func = get_function()
    file = input("Proszę podać plik z węzłami: ")
    f_desc = func['opis']
    f = func['f']
    x_nodes, y_nodes = load_nodes(f"text_files/{file}.txt", f)
    coeffs = calculate_coefficients(x_nodes, y_nodes)

    # 2. Przygotowanie danych do wykresu (tablice/wektory)
    x_plot = []
    y_orig_plot = []
    y_interp_plot = []
    x_min = x_nodes[0]
    x_length = len(x_nodes)
    x_max = x_nodes[x_length -1]
    num_points = 500
    step = (x_max - x_min) / (num_points - 1)
    current_x = x_min
    i = 0
    while i < num_points:
        x_plot.append(current_x)
        y_orig_plot.append(f(current_x))
        y_interp_val = evaluate_newton(coeffs, current_x, x_nodes)
        y_interp_plot.append(y_interp_val)
        current_x += step
        i += 1
    draw(x_plot, y_orig_plot, y_interp_plot, x_nodes, y_nodes, f_desc)

# Standardowe uruchomienie
if __name__ == "__main__":
    main()


