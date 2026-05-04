import random
from typing import Callable
from functions import FunctionData
from UI import get_function
from newton import calculate_coefficients, evaluate_newton
from graph import draw
from load_nodes import load_nodes


def main() -> None:
    # Pobieramy dane wybranej funkcji
    func: FunctionData = get_function()
    f_desc: str = func['opis']
    f: Callable[[float], float] = func['f']

    print("\n--- Wybór źródła węzłów ---")
    print("1. Wczytaj z pliku")
    print("2. Generuj losowo w przedziale")
    choice: str = input("Wybierz opcję (1/2): ")

    x_nodes: list[float] = []
    y_nodes: list[float] = []

    if choice == '1':
        file_name: str = input("Proszę podać nazwę pliku: ")
        x_nodes, y_nodes = load_nodes(f"text_files/{file_name}.txt", f)
    else:
        n: int = int(input("Podaj liczbę węzłów: "))
        a: float = float(input("Podaj początek przedziału (a): "))
        b: float = float(input("Podaj koniec przedziału (b): "))
        step = (b - a) / (n - 1)
        jitter_limit = step * 0.2
        x_nodes = []
        for i in range(n):
            base_x = a + i * step
            shift = random.uniform(-jitter_limit, jitter_limit)
            final_x = max(a, min(b, base_x + shift))
            x_nodes.append(final_x)
        x_nodes.sort()
        y_nodes = [f(x) for x in x_nodes]

    coeffs: list[float] = calculate_coefficients(x_nodes, y_nodes)

    x_plot: list[float] = []
    y_orig_plot: list[float] = []
    y_interp_plot: list[float] = []

    x_min: float = x_nodes[0]
    x_max: float = x_nodes[-1]
    num_points: int = 500
    step: float = (x_max - x_min) / (num_points - 1)

    for i in range(num_points):
        current_x: float = x_min + i * step
        x_plot.append(current_x)
        y_orig_plot.append(f(current_x))

        y_interp_val: float = evaluate_newton(coeffs, current_x, x_nodes)
        y_interp_plot.append(y_interp_val)

    draw(x_plot, y_orig_plot, y_interp_plot, x_nodes, y_nodes, f_desc)


if __name__ == "__main__":
    main()
