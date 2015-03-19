# coding=utf-8
trpBase = ''  # трипл. строка
tools = []  # все инструменты (с повторами)
entries = []  # инструменты (без повторов) и количество их вхождений
baseFile = 'VSP_00001.txt'  # база

try:
    base = open(baseFile, 'r', encoding="utf-8")
    for line in base:
        if line[13] == '$':  # если в строке файла содержатся триплеты
            trpBase += line[13:-1]  # общая трипл. строка
    base.close()
except FileNotFoundError:  # если файл отсутствует
    input('Файл не найден')
    exit()
except UnicodeDecodeError:
    input('Неверная кодировка файла. Используйте utf-8')
    exit()
trpBase = trpBase.split(';')  # разбиение трипл. строки на отдельные триплеты
for i in range(len(trpBase)):
    trpBase[i] += ';'
    if trpBase[i].split('=')[0][::-1][:4][::-1] in ('E.NM', 'W.NM'):  # выборка инструментов ($E.NM, $W.NM)
        tools += [trpBase[i]]

# СОРТИРОВКА МЕТОДОМ ПОДСЧЁТА (?)
sTools = []
k = 0
for i in range(0, len(tools)):
    c = 0
    sTools.append(int(c))
for i in range(0, len(tools)):
    for j in range(0, len(tools)):
        if tools[i] > tools[j]:
            k += 1
        elif tools[i] == tools[j] and i < j:
            k += 1
    sTools[k] = tools[i]
    k = 0

j = None
for i in range(len(sTools)):
    if sTools[i] == j:  # выборка повторяющихся инструментов
        continue
    j = sTools[i]
    print('-----------\nИнструмент: {0}\nВхождений:  {1}'.format(sTools[i], sTools.count(tools[i])))
input()
