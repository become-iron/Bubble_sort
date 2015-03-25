# coding=utf-8
'''
3. В тексте после буквы Р, если она не последняя
в слове, ошибочно напечатана буква А вместо О.
Внести исправления в текст.
'''
symbol1 = 'Р'  # символ, относительно кот-го ориентируемся
symbol2 = 'А'  # символ, кот. заменяем
symbol3 = 'О'  # символ, на кот. заменяем
file = '1.txt'  # файл, из кот-го считываем
text = ''  # текст из файла

# ЧТЕНИЕ ФАЙЛА
try:
    with open(file, 'r', encoding='utf-8') as fileContent:
        text = fileContent.read()
        fileContent.close()
except FileNotFoundError:  # если файл не найден
    input('Файл не найден')
    exit()
except UnicodeDecodeError:  # если файл сохранён в неверной кодировке
    input('Неверная кодировка файла. Используйте utf-8')
    exit()

print('ИСХОДНЫЙ ТЕКСТ:\n{0}'.format(text))  # вывод исходного текста
text = text.split(symbol1)  # разбитие строки с текстом по ранее данному символу
for i in range(1, len(text)):
    if text[i] == '':  # если элемент пустой
        text[i] = symbol1
    elif text[i][0] == symbol2:  # если элемент начинается с символа, который заменяем
        text[i] = symbol1 + symbol3 + text[i][1:]
    else:
        text[i] = symbol1 + text[i]

text = ''.join(text)  # перевод списка в строку
print('\nОТРЕДАКТИРОВАННЫЙ ТЕКСТ:\n{0}'.format(text))  # вывод отред-го текста
input('')
