import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data1.csv', names=['sepal length', 'sepal width',
                                                    'petal length', 'petal width',
                                                    'specie'])

sepal_length = df['sepal length']
sepal_width = df['sepal width']
petal_length = df['petal length']
petal_width = df['petal width']
specie = df['specie']

# Table 1
num_species = specie.value_counts()
print(num_species)
num_species_percentage = round(num_species / len(specie) * 100, 1)
print(num_species_percentage)

# Table 2
def get_statistics(name, data):
    minimum = round(data.min(), 2)
    mean = round(data.mean(), 2)
    std = round(data.std(), 2)
    median = round(data.median(), 2)
    q1 = round(data.quantile(0.25), 2)
    q3 = round(data.quantile(0.75), 2)
    maximum = round(data.max(), 2)

    print(f"{name}: {minimum} | {mean} (±{std}) | {median} ({q1} - {q3}) | {maximum}")
get_statistics('sepal length', sepal_length)
get_statistics('sepal width', sepal_width)
get_statistics('petal length', petal_length)
get_statistics('petal width', petal_width)

def get_histogram_boxplot(attribute, title, x_name):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    #Histogram
    ax1.hist(attribute, edgecolor='black')
    ax1.set_title(title)
    ax1.set_xlabel(x_name)
    ax1.set_ylabel("Liczebność")

    #Boxplot
    setosa = df[df['specie'] == 0][attribute.name]
    versicolor = df[df['specie'] == 1][attribute.name]
    virginica = df[df['specie'] == 2][attribute.name]
    ax2.boxplot([setosa, versicolor, virginica])
    ax2.set_xticklabels(['setosa', 'versicolor', 'virginica'])
    ax2.set_xlabel('Gatunek')
    ax2.set_ylabel(x_name)

    plt.tight_layout()
    plt.show()

get_histogram_boxplot(sepal_length, "Długość działki kielicha",
                      "Długość (cm)")
get_histogram_boxplot(sepal_width, "Szerokość działki kielicha",
                      "Szerokość (cm)")
get_histogram_boxplot(petal_length, "Długość płatka",
                      "Długość (cm)")
get_histogram_boxplot(petal_width, "Szerokość płatka",
                      "Szerokość (cm)")

def get_scatter(attribute_x, attribute_y, name_x, name_y):
    correlation = round(attribute_x.corr(attribute_y, method='pearson'), 2)
    a, b = np.polyfit(attribute_x, attribute_y, 1)
    a = round(a, 1)
    b = round(b, 1)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(attribute_x, attribute_y)
    ax.plot(attribute_x, a * attribute_x + b, color='red')

    if b >= 0:
        sign = '+'
    else:
        sign = '-'
    formula = f"y = {a}x {sign}{abs(b)}"
    ax.set_title(f"Pearson r = {correlation}\n{formula}")
    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)

    plt.tight_layout()
    plt.show()
get_scatter(sepal_width, sepal_length, "Szerokość działki kielicha (cm)", "Długość działki kielicha (cm)")
get_scatter(petal_length, sepal_length, "Długość płatka (cm)", "Długość działki kielicha (cm)")
get_scatter(petal_width, sepal_length, "Szerokość płatka (cm)", "Długość działki kielicha (cm)")
get_scatter(petal_length, sepal_width, "Długość płatka (cm)", "Szerokość działki kielicha (cm)")
get_scatter(petal_width, sepal_width, "Szerokość płatka (cm)", "Szerokość działki kielicha (cm)")
get_scatter(petal_width, petal_length, "Szerokość płatka (cm)", "Długość płatka (cm)")