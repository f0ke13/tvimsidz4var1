from scipy.stats import t, chi2
import math
import numpy as np

X = [-7.51, -8.65, -10.66, 2.11, -12.64, -13.16, -7.89, -3.50, 3.50, -6.32, 4.51, -2.35, -9.26, -9.45, -7.28, 0.59, -9.13, -6.92, -6.18, -4.93, -3.42, -13.32, -14.65, -1.90, -2.18, -3.03, 2.97, -5.17, -1.23, -4.74, -1.54, -8.04, -0.70, -14.92, -3.48, -1.48, 1.77, -11.60, -7.71, -4.60, -3.67, -1.00, -4.50, -4.85, -0.26, -12.07, 4.17, -0.19, -6.12, -5.09]

var_series=sorted(X)
number_of_elements = len(X)


#Мат ожидание (Выборочное среднее) (Сумма по всем элементам / количество элементов)
Expectation = sum(X) / number_of_elements 
print("Expectation is: ", Expectation)

#Выборочная Дисперсия sum(X_i-Expectation) / кол-во элементов
zapas1 = []
for j in range(number_of_elements):
    zapas1.append((X[j] - Expectation)**2)
Variance = sum(zapas1) / (number_of_elements)
print("Edited Variance is: ", Variance)

#Исправленная Выборочная Дисперсия sum(X_i-Expectation) / кол-во элементов
zapas1 = []
for j in range(number_of_elements):
    zapas1.append((X[j] - Expectation)**2)
EVariance = sum(zapas1) / (number_of_elements-1)
print("Edited Variance is: ", EVariance)

#СКО sqrt(Variance)
SKO = (Variance)**(1/2)
print("SKO is: ", SKO)

#Квантили t и chi2 (получены через scipy)
t_quantile = t.ppf(0.995, df=number_of_elements-1)
chi2_1 = chi2.ppf(0.995, df=number_of_elements-1)
chi2_2 = chi2.ppf(0.005, df=number_of_elements-1)
print("T_Quantile is: ", t_quantile)
print("Chi2_1 is: ", chi2_1)
print("Chi2_2 is: ", chi2_2)


#Побочка для вычислений доверительных интервалов
a_lower = Expectation - (t_quantile*SKO/(math.sqrt(number_of_elements-1)))
a_upper = Expectation + (t_quantile*SKO/(math.sqrt(number_of_elements-1)))
print("[",a_lower, a_upper, "]")
chislitel = number_of_elements * Variance
sigma_lower = chislitel / chi2_1
sigma_upper = chislitel / chi2_2
print("[",sigma_lower, sigma_upper, "]")
