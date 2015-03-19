# coding=utf-8
from vsptd import *
from time import sleep, strftime  # импорт функций для паузы, вывода времени

fileNameComm = 'commAgent_1652.txt'  # файл обмена
fileNameGroup = '1652.txt'  # таблица
failOper = 'ОШИБКА: операция не удалась'


def make_time():  # возвращает строку с текущим временем
    return strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S')  # ЧЧ:ММ:СС
