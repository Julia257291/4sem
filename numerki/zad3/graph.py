import matplotlib.pyplot as plt


def draw(
        x: list[float],
        y_original: list[float],
        y_interp: list[float],
        x_nodes: list[float],
        y_nodes: list[float],
        f_dsc: str
) -> None:
    plt.figure(figsize=(9, 5))

    plt.plot(x, y_original, label=f"Oryginalna: {f_dsc}", color='blue')

    plt.plot(x, y_interp, label="Funkcja interpolowana", color='red', linestyle='--')

    plt.scatter(x_nodes, y_nodes, color='black', zorder=5, label="Węzły")

    plt.title(f"Analiza interpolacji dla funkcji:\n{f_dsc}", fontsize=14, pad=15)
    plt.xlabel("Oś argumentów (x)", fontsize=12)
    plt.ylabel("Wartość funkcji f(x)", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.show()
