import numpy as np
import pandas as pd
from scipy.stats import norm, chi2

# Исходные данные
X = np.array([-7.51, -8.65, -10.66, 2.11, -12.64, -13.16, -7.89, -3.50, 3.50, -6.32, 
              4.51, -2.35, -9.26, -9.45, -7.28, 0.59, -9.13, -6.92, -6.18, -4.93, 
              -3.42, -13.32, -14.65, -1.90, -2.18, -3.03, 2.97, -5.17, -1.23, -4.74, 
              -1.54, -8.04, -0.70, -14.92, -3.48, -1.48, 1.77, -11.60, -7.71, -4.60, 
              -3.67, -1.00, -4.50, -4.85, -0.26, -12.07, 4.17, -0.19, -6.12, -5.09])

# Параметры распределения
a0 = -5
sigma0 = 5
n = len(X)
alpha = 0.01

# Исходные интервалы с наблюдаемыми частотами (low, high, freq)
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
    norm.cdf(high, loc=a0, scale=sigma0) - norm.cdf(low, loc=a0, scale=sigma0) 
    for low, high in bounds
])
expected = expected_probs * n

# Проверка условия expected >= 5
problematic_indices = np.where(expected < 5)[0]

if len(problematic_indices) > 0:
    print("Обнаружены интервалы с ожидаемой частотой < 5:")
    for idx in problematic_indices:
        low, high = bounds[idx]
        print(f"Интервал [{low}, {high}): ожидаемая частота = {expected[idx]:.2f}")
    
    print("\nРекомендации по объединению интервалов:")
    for idx in problematic_indices:
        if idx == 0:
            print(f"Объединить интервал {idx+1} ([{bounds[idx][0]}, {bounds[idx][1]}]) с интервалом {idx+2} ([{bounds[idx+1][0]}, {bounds[idx+1][1]}])")
        elif idx == len(bounds) - 1:
            print(f"Объединить интервал {idx+1} ([{bounds[idx][0]}, {bounds[idx][1]}]) с интервалом {idx} ([{bounds[idx-1][0]}, {bounds[idx-1][1]}])")
        else:
            left_exp = expected[idx-1]
            right_exp = expected[idx+1]
            if left_exp < right_exp:
                print(f"Объединить интервал {idx+1} ([{bounds[idx][0]}, {bounds[idx][1]}]) с интервалом {idx} ([{bounds[idx-1][0]}, {bounds[idx-1][1]}])")
            else:
                print(f"Объединить интервал {idx+1} ([{bounds[idx][0]}, {bounds[idx][1]}]) с интервалом {idx+2} ([{bounds[idx+1][0]}, {bounds[idx+1][1]}])")
    
    print("\nПрограмма остановлена. Пожалуйста, объедините интервалы согласно рекомендациям и запустите анализ снова.")
    exit()

# Если все интервалы подходят, продолжаем расчет
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
print("Таблица для расчета критерия хи-квадрат:")
print(df.to_string(index=False))

# Итоговые расчеты
chi2_stat = np.sum(chi2_components)
df_chi2 = len(bounds) - 1
critical_value = chi2.ppf(1 - alpha, df_chi2)
p_value = 1 - chi2.cdf(chi2_stat, df_chi2)

# Вывод результатов
print("\nРезультаты:")
print(f"Количество интервалов: {len(bounds)}")
print(f"Сумма компонентов χ²: {chi2_stat:.4f}")
print(f"Критическое значение (α={alpha}): {critical_value:.4f}")
print(f"Сумма p̂_j: {np.sum(expected_probs):.4f} (охвачено {np.sum(expected_probs)*100:.1f}% распределения)")

if chi2_stat > critical_value:
    print(f"Вывод: Гипотеза отвергается на уровне значимости {alpha}")
else:
    print(f"Вывод: Нет оснований отвергнуть гипотезу на уровне значимости {alpha}")

print(print(f"Максимальный уровень значимости, чтобы H_0 не была отвергнута: {p_value}"))
