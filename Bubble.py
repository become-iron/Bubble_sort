from random import sample #импорт функции функции для генерации рандомного числа
min = 0 #минимальное значение числа
max = 9 
values = []
amount = 5
values = sample(range(max), amount)
##for i in range(amount):
##    values+=[randint(min,max)]
    
print('Исходная последовательность: ', values)

for j in range(amount-1):
    for i in range(amount-1):
        if values[i] > values[i+1]:
            values[i], values[i+1] = values[i+1], values[i]

print('Конечная последовательность: ', values)
