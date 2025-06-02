import numpy as np
import pandas as pd
from scipy.stats import norm, chi2

# Выборка
X = np.array([-7.51, -8.65, -10.66, 2.11, -12.64, -13.16, -7.89, -3.50, 3.50, -6.32, 
              4.51, -2.35, -9.26, -9.45, -7.28, 0.59, -9.13, -6.92, -6.18, -4.93, 
              -3.42, -13.32, -14.65, -1.90, -2.18, -3.03, 2.97, -5.17, -1.23, -4.74, 
              -1.54, -8.04, -0.70, -14.92, -3.48, -1.48, 1.77, -11.60, -7.71, -4.60, 
              -3.67, -1.00, -4.50, -4.85, -0.26, -12.07, 4.17, -0.19, -6.12, -5.09])

# Параметры распределения (заготовка)
a = 0
sigma2_hat = 0
n = len(X)
alpha = 0.01

#Мат ожидание (Выборочное среднее) (Сумма по всем элементам / количество элементов)
a = sum(X) / n
print("Expectation is: ", a)

#Выборочная Дисперсия sum(X_i-Expectation) / кол-во элементов
zapas1 = []
for j in range(n):
    zapas1.append((X[j] - a)**2)
sigma2_hat = sum(zapas1) / (n)
print("Variance is: ", sigma2_hat)

theta_hat = (a, sigma2_hat)

initial_intervals = [
    (-np.inf, -11, 7),
    (-11, -7, 10),
    (-7, -5, 6),
    (-5, -3, 10),
    (-3, -1, 6),
    (-1, np.inf, 11),
]

# Разделение на границы и частоты
bounds = [(low, high) for low, high, freq in initial_intervals]
observed = np.array([freq for low, high, freq in initial_intervals])

# Вычисление ожидаемых вероятностей и частот
expected_probs = np.array([
    norm.cdf(high, loc=a, scale=np.sqrt(sigma2_hat)) - norm.cdf(low, loc=a, scale=np.sqrt(sigma2_hat)) 
    for low, high in bounds
])
expected = expected_probs * n

# Расчет компонентов хи-квадрат
chi2_components = (observed - expected)**2 / expected

# Создание DataFrame для таблицы
df = pd.DataFrame({
    '№': range(1, len(bounds) + 1),
    'Интервал': [f'({low:.1f}; {high:.1f}]' for low, high in bounds],
    'v_j': observed,
    'p̂_j': np.round(expected_probs, 4),
    'n*p̂_j': np.round(expected, 2),
    '(v_j - n*p̂_j)²': np.round((observed - expected)**2, 2),
    'χ² компонент': np.round(chi2_components, 4)
})

# Вывод таблицы
print("\nТаблица для расчета критерия хи-квадрат:")
print(df.to_string(index=False))

# Итоговые расчеты
chi2_stat = np.sum(chi2_components)
df_chi2 = len(bounds) - 1 - 2  # степени свободы
critical_value = chi2.ppf(1 - alpha, df_chi2)

# Вывод результатов
print("\nРезультаты:")
print(f"Количество интервалов: {len(bounds)}")
print(f"Сумма компонентов χ²: {chi2_stat:.4f}")
print(f"Количество степеней свободы: {df_chi2}")
print(f"Критическое значение (α={alpha}): {critical_value:.4f}")

# Проверка гипотезы
if chi2_stat > critical_value:
    print(f"Вывод: Гипотеза отвергается на уровне значимости {alpha} в пользу альтернативной")
else:
    print(f"Вывод: Нет оснований отвергнуть гипотезу на уровне значимости {alpha}")

# Дополнительная информация
check = chi2.cdf(chi2_stat, df_chi2)
print("Максимальный уровень значимости, чтобы H_0 не была отвергнута: ", 1 - check)