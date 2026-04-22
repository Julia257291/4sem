import matplotlib.pyplot as plt

def draw(x, y_original, y_interp, x_nodes, y_nodes, f_dsc):
    # Tworzymy obszar wykresu o odpowiednich wymiarach
    plt.figure(figsize=(9, 5))
    plt.plot(x, y_original, label=f"Oryginalna: {f_dsc}",
             color='blue')
    #Wykres wielomianu interpolacyjnego Newtona (czerwona linia przerywana)
    plt.plot(x, y_interp, label="Funkcja interpolowana",
             color='red')
    # zaznaczenie węzłów interpolacji
    plt.scatter(x_nodes, y_nodes, color='black', zorder=5, label="Węzły")
    plt.title(f"Analiza interpolacji dla funkcji:\n{f_dsc}", fontsize=14, pad=15)
    plt.xlabel("Oś argumentów (x)", fontsize=12)
    plt.ylabel("Wartość funkcji f(x)", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.show()