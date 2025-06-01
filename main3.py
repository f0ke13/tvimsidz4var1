from scipy import stats
from scipy.stats import t, chi2, norm, kstwobign
import math
import numpy as np
import pandas as pd

X = [-7.51, -8.65, -10.66, 2.11, -12.64, -13.16, -7.89, -3.50, 3.50, -6.32, 4.51, -2.35, -9.26, -9.45, -7.28, 0.59, -9.13, -6.92, -6.18, -4.93, -3.42, -13.32, -14.65, -1.90, -2.18, -3.03, 2.97, -5.17, -1.23, -4.74, -1.54, -8.04, -0.70, -14.92, -3.48, -1.48, 1.77, -11.60, -7.71, -4.60, -3.67, -1.00, -4.50, -4.85, -0.26, -12.07, 4.17, -0.19, -6.12, -5.09]
a0 = -5.00
sigma0 = 5.00
alpha = 0.01
X_sorted=sorted(X)
n = len(X)

print(X_sorted)
print(n)

# Создание DataFrame
df = pd.DataFrame({
    'i': range(1, n+1),
    '(i-1)/n': [(i-1)/n for i in range(1, n+1)],
    'i/n': [i/n for i in range(1, n+1)],
    'X_(i)': X_sorted,
    'F0(X_(i))': norm.cdf((np.array(X_sorted) - a0) / sigma0),
})

# Вычисление отклонений
df['ld'] = df['F0(X_(i))'] - df['(i-1)/n']
df['ud'] = df['i/n'] - df['F0(X_(i))']

# Добавление столбца с max{|ld|, |ud|}
df['max{|ld|,|ud|}'] = df[['ld', 'ud']].abs().max(axis=1)

# Нахождение максимального отклонения
Dn_plus = df['ud'].max()
Dn_minus = abs(df['ld']).max()
Dn = max(Dn_plus, Dn_minus)

# Вывод таблицы
pd.set_option('display.max_rows', None)  # Показать все строки
print(df)

# Вывод статистики Колмогорова
print(f"\nСтатистика Колмогорова: Dn = {Dn:.4f}")

# Квантиль распределения Колмогорова
critical_value = stats.kstwobign.ppf(1-alpha)
print(f"Критическое значение K_alpha при альфа={alpha}: {critical_value:.4f}")

koren = math.sqrt(n)
phi_x= koren * Dn
print(phi_x)
if phi_x <= critical_value:
    print(phi_x, " <= ", critical_value, ". Значит наблюдения не противоречат гипотезе H_0.")
else:
    print(phi_x, " > ", critical_value, ". Значит на основании вычислений и данных гипотеза H_0 отвергается в пользу альтернативной.")


#Максимальный уровень доверия
alpha_max = 1 - kstwobign.cdf(phi_x) #kstwobign - вычисляет функцию распределения Колмогорова при каком-то параметре
print(f"Минимальный уровень значимости, при котором H0 отвергается в пользу альтернативной: {alpha_max}")