from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np

X = [-7.51, -8.65, -10.66, 2.11, -12.64, -13.16, -7.89, -3.50, 3.50, -6.32, 4.51, -2.35, -9.26, -9.45, -7.28, 0.59, -9.13, -6.92, -6.18, -4.93, -3.42, -13.32, -14.65, -1.90, -2.18, -3.03, 2.97, -5.17, -1.23, -4.74, -1.54, -8.04, -0.70, -14.92, -3.48, -1.48, 1.77, -11.60, -7.71, -4.60, -3.67, -1.00, -4.50, -4.85, -0.26, -12.07, 4.17, -0.19, -6.12, -5.09]

var_series=sorted(X)
number_of_elements = len(X)

counts = Counter(X)
count_array = [counts[x] for x in X] # массив, в котором содержится количество повторов каждого элемента

print(var_series)
print(number_of_elements)

#Вычисления вероятностей для эмпирической функции распределения
for i in range(number_of_elements):
    # Вероятность = количество вхождений элемента / общее количество элементов
    probability = count_array[i] / number_of_elements
    print(f"Probability of {X[i]:.2f}: {probability:.4f}")

#Мат ожидание (Выборочное среднее) (Сумма по всем элементам / количество элементов)
Expectation = sum(X) / number_of_elements 
print("Expectation is: ", Expectation)

#Выборочная Дисперсия sum(X_i-Expectation) / кол-во элементов
zapas1 = []
for j in range(number_of_elements):
    zapas1.append((X[j] - Expectation)**2)
Variance = sum(zapas1) / (number_of_elements)
print("Variance is: ", Variance)

#СКО sqrt(Variance)
SKO = (Variance)**(1/2)
print("SKO is: ", SKO)

#Медиана
index1 = int((number_of_elements / 2) - 1) #24
index2 = int(number_of_elements / 2) #25
Me = (var_series[index1] + var_series[index2])/2
print("Median is: ", Me)

#Асимметрия
zapas2 = []
for j in range(number_of_elements):
    zapas2.append((X[j] - Expectation)**3)
mu_3 = sum(zapas2) / (number_of_elements-1)
s_3 = SKO**3  # стандартное отклонение в кубе
As = mu_3 / s_3 
print("Asymmetry is: ", As)

#Эксцесс
zapas3 = []
for j in range(number_of_elements):
    zapas3.append((X[j] - Expectation)**4)
mu_4 = sum(zapas3) / (number_of_elements-1)
s_4 = SKO**4
Es = (mu_4/s_4) -3
print(mu_4, s_4)
print("Excess is: ", Es)


#Вероятности P(X \in [c,d]) c = -8, d = -2
c = -8.00
d = -2.00
count_in_interval = 0
for i in range (50):
    if c <= var_series[i] <= d:
        count_in_interval += 1
prob_in_interval = count_in_interval / number_of_elements
print("Probability in Interval [c,d]: ", prob_in_interval)

h = 2
start = -15
bins = np.arange(start, max(X) + h, h)  # Создаем интервалы с шагом h

# Строим гистограмму
plt.figure(figsize=(12, 6))
plt.hist(X, bins=bins, edgecolor='black', alpha=0.7, label='Гистограмма', density=False)

# Строим полигон частот
# Для полигона нужно вычислить середины интервалов и частоты
hist, bin_edges = np.histogram(X, bins=bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  # середины интервалов

# Добавляем точки на границах для правильного отображения полигона
bin_centers = np.concatenate([[bin_centers[0] - h], bin_centers, [bin_centers[-1] + h]])
hist = np.concatenate([[0], hist, [0]])

plt.plot(bin_centers, hist, 'r-', marker='o', label='Полигон частот')

# Настройка графика
plt.title('Гистограмма и полигон частот (h=2)')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.xticks(bins)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()