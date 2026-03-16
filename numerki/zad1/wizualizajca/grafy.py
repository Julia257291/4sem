import matplotlib.pyplot as plt

def generate_plot_data(func, a, b, num_points=150):
    x_vals = []
    y_vals = []
    step = (b -a) / num_points
    x_current =a
    i = 0
    while i < num_points:
        x_vals.append(x_current)
        y_vals.append(func(x_current))
        x_current += step
        i += 1
    return x_vals, y_vals

def draw_plot(x_vals, y_vals, roots):
    plt.figure(figsize=(9, 5))
    plt.plot(x_vals, y_vals, label="f(x)", color="black", linewidth=2)
    plt.axhline(0, color='black', linewidth=1.2, linestyle='--')
    colors = ['red', 'green']
    i = 0
    while i < 2:
        c = colors[i]
        plt.scatter([roots[i]], [0], color=c, zorder=5, s=75, edgecolors='black',
                    label=f"Miejsce zerowe: {roots[i]:.8f}")
        i += 1

    plt.title("Wykres funkcji i jej miejsc zerowych", fontsize=14)
    plt.xlabel("Oś X", fontsize=12)
    plt.ylabel("Wartość f(x)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.legend()

    plt.show()