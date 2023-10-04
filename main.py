import numpy as np

comma = ','

#погрешности
x_errors = 0
y_errors = 10**(-3)

#до какого знака после запятой?
accuracy = 3


#а что изучаем?
x_what = 'глубина модуляции'
x_what_exactly = '\\'+'m'
x_what_a_unit = '\\'+'text{усл.ед.}'
y_what = 'отношение амплитуд'
y_what_exactly = '\\'+'cfrac', '{a_1}{a_2}'
y_what_a_unit = '\\'+'text{усл.ед.}'

#загружаем данные из файла в список
data_list = []
with open("data.txt") as f:
    for line in f:
        data_list.append([float(x) for x in line.split()])

#для удобства создаём массив
data_array = np.array(data_list)

x = []
y = []
for i in range(0, len(data_list)):
    x.append(float(data_array[i,0]))
    y.append(float(data_array[i,1]))

x_min = min(x)
x_max = max(x)
y_min = min(y)
y_max = max(y)

"""
l_x = len(str((x_min + x_max)/ 2))
if x_min < 1:
    delta_x =
"""

#выводим таблицу с данными:

print('\\' + 'begin{center}')
print('\\' + 'begin{tabular}{', end = '')
for i in range(0, len(data_list) + 1):
    print('|c', end = '')
print('|}')
print('\\' + 'hline')
print('$', 'something',  '$ ', end = '')
for i in range(0, len(data_list)):
    print('&', x[i], ' ', end = '')
print('\\' + '\\')
print('\\' + 'hline')
print('$', 'something', '$ ', end = '')
for i in range(0, len(data_list)):
    print('&', y[i], ' ', end='')
print('\\' + '\\')
print('\\' + 'hline')
print('\\' + 'end{tabular}')
print('\\' + 'end{center}')

#выводим шапку графика:

print("\\" + 'begin{center}')
print("\\" + 'begin{tikzpicture}')
print("\\" + 'begin{axis}')
print(""" [
minor xtick={0},
minor ytick= {0},""")
print('\t', 'grid=major,')
print('\t', 'title = Зависимость...', comma)
print('\t', 'xlabel = {$', '\\' + 'text{something}', '$},')
print('\t', 'ylabel = {$', '\\' + 'text{something}', '$},')
print('\t', 'legend style={at={(0,1)},anchor=north west},')
print('\t', 'minor tick num = 2')
print('\t', 'ymax = 0.5')
print(']')

print("\\" + "addplot + [only marks,")
print("""error bars/.cd,  y dir=both,y explicit, 
x dir=both,x explicit] coordinates {
""")

for i in range(0, len(data_list)):
    print('(', data_array[i,0], ',', data_array[i,1], ')', '+-', '(', x_errors, ',', y_errors, ')' )

print("""
};""")
print('\\' + "addplot[experiment1] table {")
print('x', 'y')

#линейная аппроксимация

A = np.vstack([x, np.ones(len(x))]).T
k, b = np.linalg.lstsq(A, y, rcond=None)[0]

def approx(number):
    return k*number + b

#найдём погрешности коэффициентов
d_k = 0
d_b = 0
#дисперсия y
summ_dyy_squared = 0
for i in range(0, len(data_list)):
    summ_dyy_squared += (y[i] - approx(x[i]))**2
d_yy = summ_dyy_squared/len(data_list)
#дисперсия x
summ_dxx_squared = 0
for i in range(0, len(data_list)):
    summ_dxx_squared += (x[i] - (y[i] - b)/k)**2
d_xx = summ_dxx_squared/len(data_list)
#средний квадрат x
summ_xx_squared = 0
for i in range(0, len(data_list)):
    summ_xx_squared += x[i]**2
#погрешность k
d_k = ((1/(len(data_list) - 2))*abs((((d_yy)/(d_xx)) - k**2)))**0.5

#погрешность b
d_b = d_k * ((summ_xx_squared)**0.5)

print(x_min, approx(x_min))
print(x_max, approx(x_max))
print('};')
print("\\" + 'end{axis}')
print("\\" + 'end{tikzpicture}')
print("\\" + 'end{center}')

if (x_errors <= (x_max - x_min)/120) or (y_errors <= (y_max - y_min)/100):
    print('Кресты погрешностей не помещаются на график в выбранном масштабе.')
print('МНК получаем:')
print('\\' + 'begin{equation}')
if not ((1 <= d_k < 10) and (1 <= d_b < 10)):
    k_power = np.log10(abs(k)) // 1
    b_power = np.log10(abs(b)) // 1
    print('y', '=', round(k * (10 ** (-k_power)), accuracy), '* 10^', int(k_power), '\\' + 'cfrac{', '\\' + 'text{', y_what_a_unit, '}}{', '\\' + 'text{', x_what_a_unit, '}} *', 'x', '+', round(b * (10 ** (-b_power)), accuracy), '* 10^', int(b_power), y_what_a_unit)
else:
    print('y', '=', k, '\\' + 'cfrac{', '\\' + 'text{', y_what_a_unit, '}}{', '\\' + 'text{', x_what_a_unit, '}} *', x_what_exactly, '+', b, y_what_a_unit)


print('\\' + 'end{equation}')
print()

#округлим чиселки
"""
if not ((1 <= d_k < 10) or (1 <= d_b < 10)):
    d_k_power = np.log10(abs(d_k)) // 1
    d_b_power = np.log10(abs(d_b)) // 1
    print('$$\sigma_k = ', round(d_k * (10 ** (-d_k_power)), accuracy), '* 10^', int(d_k_power), '$$')
    print()
    print('$$\sigma_b = ', round(d_b * (10 ** (-d_b_power)), accuracy), '* 10^', int(d_b_power), '$$')
else:
    print('$$\sigma_k = ', d_k, '$$')
    print('$$\sigma_b = ', d_b, '$$')
"""

#попытка посчитать погрешности
m = [i for i in range(len(data_list))]
m_small = -1000000
m_big = 1000000
for i in range(0, len(data_list)):
    m[i] = y[i] - k * x[i] - b
    if m[i] > m_small:
        m_small = m[i]
    if m[i] < m_big:
        m_big = m[i]

delta_b = 0.5*(m_small - m_big)

b_max = 0
for i in range(0, len(data_list)):
    if y[i] > k * x[i] + b_max:
        b_max = y[i] - k * x[i]
delta_k = abs(((k * x_max + b_max - b)/x_max) - k)

print('$$', '\\' + 'Delta', 'b =', delta_b, y_what_a_unit, '$$')
print('$$', '\\' + 'Delta', 'k =', delta_k, y_what_a_unit, '/', x_what_a_unit, '$$')
