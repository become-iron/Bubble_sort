# coding=utf-8
from same import *

contentTable = []  # list для хранения таблицы

print('Агент 1 запущен: ', make_time())
# запись таблицы в list, на каждого человека - отдельный элемент (трипл. строка)
base = open('base.txt', 'r')
baseContent = base.read().split(',')
base.close()

table = open(fileNameGroup, 'r')
for line in table:
    contentTableTemp = line[:-1].split(';')
    contentTable += [trpAddStr('', baseContent[0], baseContent[1], contentTableTemp[0])[1] +
                     trpAddStr('', baseContent[0], baseContent[2], contentTableTemp[1])[1] +
                     trpAddStr('', baseContent[0], baseContent[3], contentTableTemp[2])[1] +
                     trpAddStr('', baseContent[0], baseContent[4], contentTableTemp[3])[1]]
table.close()
print('Taблица успешно обработана: ', make_time())
while True:
    result = -1
    file = open(fileNameComm, 'r')
    contentFile = file.read()
    file.close()

    if contentFile == '':  # если файл пустой
        sleep(1)
    elif contentFile != result:
        print('============================')
        print('Принят запрос: ', make_time())
        print(contentFile)  # содержимое запроса
        try:
            try:
                triplet1 = (trpGetName(contentFile)[1], trpGet(contentFile, '\u0053', trpGetName(contentFile)[1])[1],)
                triplet2 = (trpGetName(trpDel(contentFile, '\u0053', triplet1[0])[1])[1],)

                for i in range(len(contentTable)):
                    tripletValueTemp = trpGet(contentTable[i], '\u0053', triplet1[0])
                    if tripletValueTemp[0] == 0:
                        if tripletValueTemp[1] == triplet1[1]:
                            tripletValueTemp2 = trpGet(contentTable[i], '\u0053', triplet2[0])
                            if tripletValueTemp2[0] == 0:
                                result = trpAddStr(trpAddStr('', '\u0053', triplet2[0], tripletValueTemp2[1])[1], '\u0053',
                                                   triplet1[0], triplet1[1])[1]
                                break
                            else:
                                result = failOper
                                break
                        else:
                            continue
            except ValueError:  # обработка ошибки, возникающей при работе с модулем vsptd
                result = -1
        except:
            result = -1
        if result == -1:
            result = failOper  # ошибка

        print('Отправлен ответ: ', make_time())
        print(result)
        with open(fileNameComm, 'w') as file:
            file.write(result)
            file.close()
        sleep(1)
