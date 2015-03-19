# coding=utf-8
from vsptd import *  # импортирование модуля для работы с ВСПТД

trpStrs = []  # list для хранения всех триплексных строк
# сообщения при ошибках
failOper = 'ОШИБКА: Операция не удалась'
notNumber = 'ОШИБКА: Введите число'
wrongCommand = 'ОШИБКА: Неверная команда'
wrongIndex = 'ОШИБКА: Неверный индекс'
sameIndex = 'ОШИБКА: Одинаковые индексы'


# проверка, являются ли вводимые данные числом
def is_number(q):
    try:
        float(q)
        return True
    except ValueError:
        return False


# вывод меню и ввод команды
def get_menu():
    global menuCmd
    print('=====================================\n'
          'Введите номер нужной команды:\n'
          '1. Прочитать триплет\n'
          '2. Добавить триплет\n'
          '3. Удалить триплет\n'
          '4. Прочитать триплексную строку\n'
          '5. Добавить триплексную строку\n'
          '6. Объединить две триплексные строки\n'
          '7. Удалить триплексную строку')
    menuCmd = input()
    if is_number(menuCmd) is True:
        menuCmd = int(menuCmd)
    else:
        menuCmd = -1


while True:
    get_menu()

    # Прочитать триплет
    if menuCmd == 1:
        print('Триплексных строк: ' + str(len(trpStrs)))
        if len(trpStrs) == 0:  # если нет трипл. строк
            continue
        elif len(trpStrs) == 1:  # если одна трипл. строка
            gottenValue = trpSplit(trpStrs[0])
            print('Элементов в триплексной строке: ' + str(len(gottenValue)))
            if len(gottenValue) == 1:  # если в трипл. строке один триплет
                print(gottenValue[0])
            else:
                value = input('Выберите нужный элемент: ')
                if is_number(value) is True:
                    value = int(value)
                    try:
                        print(gottenValue[value])
                    except IndexError:
                        print(wrongIndex)
                else:
                    print(notNumber)
        else:
            value = input('Введите нужную строку: ')
            if is_number(value) is True:
                value = int(value)
                try:
                    gottenValue = trpSplit(trpStrs[value])
                    print('Элементов в триплексной строке: ' + str(len(gottenValue)))
                    if len(gottenValue) == 1:  # если в трипл. строке один элемент
                        print(gottenValue[0])
                        continue
                    elif len(gottenValue) == 0:  # если в трипл. строке нет элементов
                        continue
                    value2 = input('Выберите нужный элемент: ')
                    if is_number(value) is True:
                        value2 = int(value2)
                        try:
                            print(gottenValue[value2])
                        except IndexError:
                            print(wrongIndex)
                    else:
                        print(notNumber)
                except IndexError:
                    print(wrongIndex)
            else:
                print(notNumber)

    # Добавить триплет
    elif menuCmd == 2:
        print('Триплексных строк: ' + str(len(trpStrs)))
        if len(trpStrs) == 0:  # если нет ни одной триплексной строки
            print('Нет ни одной трипл. строки. Будет создана новая')
            gottenValue = trpAddStr('', input('Prefix: '), input('Name: '), input('Value: '))
            if gottenValue[0] == -1:
                print(failOper)
            else:
                trpStrs += [gottenValue[1]]
                print(trpStrs[0])
        elif len(trpStrs) == 1:  # если есть только одна трипл. строка
            gottenValue = trpAddStr(trpStrs[0], input('Prefix: '), input('Name: '), input('Value: '))
            if gottenValue[0] == -1:
                print(failOper)
            else:
                trpStrs[0] = gottenValue[1]
                print(trpStrs[0])
        else:  # если есть >= 2 трипл. строк
            print('Триплексных строк: ' + str(len(trpStrs)))
            value = input('Выберите нужную: ')
            if is_number(value) is True:
                value = int(value)
                gottenValue = trpAddStr(trpStrs[value], input('Prefix: '), input('Name: '), input('Value: '))
                if gottenValue[0] == -1:
                    print(failOper)
                else:
                    trpStrs[value] = gottenValue[1]
                    print(trpStrs[value])
            else:
                print(notNumber)

    # Удалить триплет
    elif menuCmd == 3:
        print('Триплексных строк: ' + str(len(trpStrs)))
        if len(trpStrs) == 0:  # если нет трипл. строк
            continue
        elif len(trpStrs) == 1:  # если одна трипл. строка
            gottenValue = trpSplit(trpStrs[0])
            print('Триплетов: ' + str(len(gottenValue)))
            value = input('Введите номер нужного триплета: ')
            if is_number(value) is True:
                try:
                    del(gottenValue[value])
                    trpStrs[value] = gottenValue[1:-1]
                    print('Триплет удалён')
                except IndexError:
                    print(wrongIndex)
            else:
                print(notNumber)
        else:
            value = input('Введите номер нужной триплексной строки: ')
            if is_number(value) is True:
                value = int(value)
                gottenValue = trpSplit(trpStrs[value])
                print('Триплетов: ' + str(len(gottenValue)))
                value2 = input('Введите номер нужного триплета: ')
                if is_number(value2) is True:
                    try:
                        del(gottenValue[value2])
                        trpStrs[value] = gottenValue[1:-1]
                        print('Триплет удалён')
                    except IndexError:
                        print(wrongIndex)
                else:
                    print(notNumber)
            else:
                print(notNumber)

    # Прочитать триплексную строку
    elif menuCmd == 4:
        print('Триплексных строк: ' + str(len(trpStrs)))
        if len(trpStrs) == 0:  # если нет трипл. строк
            continue
        elif len(trpStrs) == 1:  # если одна трипл. строка
            print(trpStrs[0])
        else:
            value = input('Введите номер нужной трипл. строки: ')
            if is_number(value) is True:
                value = int(value)
                try:
                    print(trpStrs[value])
                except IndexError:
                    print(wrongIndex)
            else:
                print(notNumber)

    # Добавить триплексную строку
    elif menuCmd == 5:
        trpStrs += ['']
        print('Триплексная строка №' + str(len(trpStrs)) + ' добавлена')

    # Объединить две триплексные строки
    elif menuCmd == 6:
        print('Триплексных строк: ' + str(len(trpStrs)))
        if len(trpStrs) < 2:  # если трипл. строк <2
            continue
        elif len(trpStrs) == 2:  # если трипл. строк 2
            gottenValue = trpMergeStr(trpStrs[0], trpStrs[1])
            if gottenValue[0] == -1:
                print(failOper)
            else:
                trpStrs[0] = gottenValue[1]
                del(trpStrs[1])
                print('Триплексные строки объединены: ' + trpStrs[0])
        else:
            value = input('Номер первой триплексной строки: ')
            value2 = input('Номер второй триплексной строки: ')
            if is_number(value) is True and is_number(value2) is True:
                if value == value2:
                    print(sameIndex)
                    continue
                value = int(value)
                value2 = int(value2)
                try:
                    gottenValue = trpMergeStr(trpStrs[value], trpStrs[value2])
                    if gottenValue[0] == -1:
                        print(failOper)
                    else:
                        trpStrs[value] = gottenValue[1]
                        del(trpStrs[value2])
                        print('Триплексные строки объединены: ' + trpStrs[value])
                except IndexError:
                    print(wrongIndex)
            else:
                print(notNumber)

    # Удалить триплексную строку
    elif menuCmd == 7:
        print('Триплексных строк: ' + str(len(trpStrs)))
        value = input('Введите номер нужной трипл. строки: ')
        if is_number(value) is True:
            value = int(value)
            del(trpStrs[value])
            print('Трипл. строка удалена')
        else:
            print(notNumber)

    elif menuCmd == -1:
        print(notNumber)

    else:
        print(wrongCommand)
