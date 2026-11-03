import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

df = pd.read_csv('data1.csv', names=['sepal length', 'sepal width',
                                     'petal length', 'petal width', 'specie'])

species_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

sepal_length = df['sepal length']
sepal_width = df['sepal width']
petal_length = df['petal length']
petal_width = df['petal width']
specie = df['specie']

# Table 1
num_species = specie.value_counts()

num_species_percentage = round(num_species / len(specie) * 100, 1)

for index in num_species.index:
    count = num_species[index]
    percentage = num_species_percentage[index]
    name = species_names[index]
    print(f"Gatunek {name}: {count} ({percentage}%)")

print("----------------------------")

# Table 2
labels = {
    'sepal length': 'Długość działki kielicha (cm)',
    'sepal width': 'Szerokość działki kielicha (cm)',
    'petal length': 'Długość płatka (cm)',
    'petal width': 'Szerokość płatka (cm)'
}

def get_statistics(name, data):
    minimum = round(data.min(), 2)
    mean = round(data.mean(), 2)
    std = round(data.std(), 2)
    median = round(data.median(), 2)
    q1 = round(data.quantile(0.25), 2)
    q3 = round(data.quantile(0.75), 2)
    maximum = round(data.max(), 2)

    print(f"{name}: {minimum:.2f} | {mean:.2f} (±{std:.2f}) | {median:.2f} ({q1:.2f} - {q3:.2f}) | {maximum:.2f}")

for col_en, col_pl in labels.items():
    get_statistics(col_pl, df[col_en])

print("----------------------------")

# Task 3
def get_histogram_boxplot(attribute, title, x_name, ax1, ax2):
    bin_width = 0.5
    min_val = np.floor(attribute.min() / bin_width) * bin_width
    max_val = np.ceil(attribute.max() / bin_width) * bin_width

    bins = np.arange(min_val, max_val + bin_width, bin_width)

    ax1.hist(attribute, bins=bins, edgecolor='black')
    ax1.set_title(title)
    ax1.set_xlabel(x_name)
    ax1.set_ylabel("Liczebność")
    ax1.set_xticks(bins)

    setosa = df[df['specie'] == 0][attribute.name]
    versicolor = df[df['specie'] == 1][attribute.name]
    virginica = df[df['specie'] == 2][attribute.name]

    ax2.boxplot([setosa, versicolor, virginica])
    ax2.set_xticklabels(list(species_names.values()))
    ax2.set_xlabel('Gatunek')
    ax2.set_ylabel(x_name)

fig3, axes3 = plt.subplots(nrows=4, ncols=2, figsize=(10, 12))
fig3.subplots_adjust(hspace=0.6)

get_histogram_boxplot(sepal_length, "Długość działki kielicha",
                      "Długość (cm)", axes3[0, 0], axes3[0, 1])
get_histogram_boxplot(sepal_width, "Szerokość działki kielicha",
                      "Szerokość (cm)", axes3[1, 0], axes3[1, 1])
get_histogram_boxplot(petal_length, "Długość płatka",
                      "Długość (cm)", axes3[2, 0], axes3[2, 1])
get_histogram_boxplot(petal_width, "Szerokość płatka",
                      "Szerokość (cm)", axes3[3, 0], axes3[3, 1])

plt.savefig('wykres3')

# Task 4
def get_scatter(attribute_x, attribute_y, name_x, name_y, ax):
    correlation = round(attribute_x.corr(attribute_y, method='pearson'), 2)
    a, b = np.polyfit(attribute_x, attribute_y, 1)
    a = round(a, 1)
    b = round(b, 1)

    ax.scatter(attribute_x, attribute_y)
    ax.plot(attribute_x, a * attribute_x + b, color='red')

    if b >= 0:
        sign = '+'
    else:
        sign = '-'
    formula = f"y = {a}x {sign} {abs(b)}"

    ax.set_title(f"Pearson r = {correlation}\n{formula}")
    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)


features = list(labels.keys())
pairs = list(combinations(features, 2))

fig4, axes4 = plt.subplots(nrows=3, ncols=2, figsize=(10, 12))
fig4.subplots_adjust(hspace=0.5)

for (col_x, col_y), ax in zip(pairs, axes4.flatten()):
    attr_x = df[col_x]
    attr_y = df[col_y]

    name_x = labels[col_x]
    name_y = labels[col_y]

    get_scatter(attr_x, attr_y, name_x, name_y, ax)

plt.savefig('wykres4')
