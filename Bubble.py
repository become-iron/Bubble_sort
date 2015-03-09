# coding=utf-8
# сортировка пузырьком
values = []  # список для хранения значений
while True:
    try:  # исключение
        # ввод количества принимаемых значений
        amount = int(input('\nВведите количество: '))

        # ввод значений
        for i in range(amount):
            print('Введите', i + 1, 'значение: ')
            values += [input()]

        print('Исходная последовательность: ', values)

        # сортировка
        for j in range(amount - 1):
            for i in range(amount - 1):
                if values[i] > values[i + 1]:
                    values[i], values[i + 1] = values[i + 1], values[i]

        print('Конечная последовательность: ', values)

    # сообщение об ошибке при попытке ввести не число
    # в графе количества принимаемых значений
    except ValueError:
        print('Введите число')
