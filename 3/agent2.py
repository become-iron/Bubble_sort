# coding=utf-8
from same import *

print('Агент 2 запущен: ', make_time())
query = ''
with open(fileNameComm, 'w') as file:  # очистка файла
    pass
while True:
    file = open(fileNameComm, 'r')
    contentFile = file.read()
    file.close()
    if contentFile == '':  # если файл пустой
        print('============================')
        print('Введите запрос вида "$S.FAM=\'Иванов\';$S.IO=:;":')
        query = '$' + input('Prefix: ').upper().strip() + '.' + \
                input('Name: ').upper().strip() + '=\'' + \
                input('Value: ').strip() + '\';' + \
                '$' + input('Prefix2: ').upper().strip() + '.' + \
                input('Name2: ').upper().strip() + '=:;'

        # проверка корректности введённых данных
        if trpCheck(query) == 0:
            print('Запрос корректен')
            # запись команды в файл
            with open(fileNameComm, 'w') as file:
                file.write(query)
            print('Запрос отправлен: ', make_time())
            print(query)
        else:
            print('Некорректный запрос')
            continue

    else:
        if contentFile == query:  # если в файле содержится та же команда, что и передавали
            sleep(1)
        else:
            print('Принят ответ:', make_time(), '\n', contentFile)  # вывод содержимого файла
            with open(fileNameComm, 'w') as file:  # очистка файла
                pass
