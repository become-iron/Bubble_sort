# Зарезервированные символы ВСПТД:
trpBeg = '$'; # Начало триплета.
trpEnd = ';'; # Конец триплета.
trpAps = '\''; # Начало и конец текстового значения.
trpKv = '\"'; # Начало и конец комментария.
trpPoint = '.'; # Точка, разделяющая префикс и имя триплета.
trpEqual = '='; # Знак присваивания.
trpRequest = ':'; # Запрос.

systemSymbols = [trpBeg, trpEnd, trpAps, trpKv, trpPoint, trpEqual, trpRequest];

def trpAddStr(trpStr, prefix, name, value, typeValue = 1, rem = ""):
    '''
    Добавляет триплет в триплетную строку по лексикографическому возрастанию префиксов триплетов.
    
    Параметры:
        trpStr - триплексная строка, в которую производится добавление;
        prefix - префикс добавляемого триплета;
        name - имя добавляемого триплета;
        value - значение добавляемого триплета;
        typeValue - тип значения триплета:
            0 - числовое значение;
            1 - текстовое значение (заключается в апострофы);
        rem - комментарий к добавляемому триплету.
    '''
    try:
        if (int(typeValue) not in [0, 1]):
            return (-1,);
    except ValueError:
        return (-1,);

    if (typeValue == 0):
        try:
            value = int(value);
        except ValueError:
            return (-1,);
    else:
        value = str(value);

    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    prefix = str(prefix);
    name = str(name);
    rem = str(rem);
    
    currentIndex = 0; # Текущий индекс при проходе по триплексной строке.
    lenStr = len(trpStr); # Длина триплексной строки.

    # Формирование добавляемого триплета.
    triplet = trpBeg + prefix + trpPoint + name + trpEqual;
    if (typeValue == 0):
        triplet += str(value);
    else:
        triplet += trpAps + value + trpAps;
    if (rem != ""): triplet += trpKv + rem + trpKv;
    triplet += trpEnd;

    while(currentIndex < lenStr):

        tmp = trpStr[currentIndex:]; # Часть строки, начинающаяся с текущего индекса.
        
        # Получение префикса и имени текущего триплета.
        currentPrefix = trpGetPrefix(tmp)[1];
        currentName = trpGetName(tmp)[1];
            
        # Вставка триплета.
        if (currentPrefix >= prefix):
            # 1. Вставка с заменой (если триплет с такими же префиксом и именем уже есть в исходной строке).
            if (currentPrefix == prefix and currentName == name): 
                lenOld = trpStr[currentIndex:].index(trpEnd) + 1; # Длина заменяемого триплета.
                res = trpStr[:currentIndex] + triplet + trpStr[currentIndex + lenOld:];
                return (0, res);

            # 2. Вставка с добавлением (если такого же трилета в исходной строке нет).
            res = trpStr[:currentIndex] + triplet + trpStr[currentIndex:];
            return (0, res);
                          
        currentIndex = trpGoNext(trpStr, currentIndex + 1)[1]; # Переход к следующему триплету.

    res = trpStr + triplet; # Добавление триплета в конец строки.
    return (0, res);

def trpCheck(trpStr):
    '''
    Проверка корректности триплексной строки.

    Коды ошибок:
    1 - между триплетами есть посторонние символы;
    2 - попытка начать новый триплет при незакрытом предыдущем или отсутствие конца последнего триплета;
    3 - отсутствие префикса триплета;
    4 - некорректный префикс;
    5 - не задано имя триплета;
    6 - наличие недопустимых символов в имени триплета (или отсутствие знака присваивания);
    7 - отсутствие закрывающего апострофа в значении триплета;
    8 - строковое значение триплета не обрамлено в апострофы;
    9 - наличие посторонних символов после значения триплета, не оформленных в комментарий;
    10 - отсутствие закрывающей кавычки в комментарии (или есть посторонние символы после комментария).

    Параметры:
        trpStr - проверяемая строка.
    '''
    # ПЕРВЫЙ ЭТАП ПРОВЕРКИ: можно ли строку корректно разбить на триплеты?
    
    inTrp = 0; # Увеличивается на 1 при входе в триплет и уменьшается на 1 при выходе из него.
    
    trpStr = str(trpStr);
    lenStr = len(trpStr); # Количество символов в строке.

    i = 0;
    while (i < lenStr):

        if (trpStr[i] == trpBeg): inTrp += 1;
        if (trpStr[i] == trpEnd): inTrp -= 1;
                
        if (inTrp == 0):
            if (trpStr[i] not in [trpEnd, " ", "\n", "\0"]):
                return 1; # Ошибка: посторонние символы между триплетами.
            else:
                if (trpStr[i] != trpEnd):
                    trpStr = trpStr[:i] + trpStr[i+1:];
                    lenStr -= 1;
                    i -= 1;
                
        if (abs(inTrp) > 1 or (inTrp != 0 and i == lenStr - 1)):
            return 2; # Ошибка: несоответствие начала и конца триплета (начало нового триплета при незакрытом предыдущем).

        i += 1;

    triplets = trpSplit(trpStr); # Разбиение строки на отдельные триплеты.
    kolTrp = len(triplets);

    for i in range(kolTrp):
        # ВТОРОЙ ЭТАП ПРОВЕРКИ: проверка синтаксиса каждого триплета.
        isTrpRegular = tripletCheck(triplets[i]);
        if (isTrpRegular != 0):
            return isTrpRegular;

    return 0;

def tripletCheck(trpStr):
    '''
    Проверка триплета.

    Параметры:
        trpStr - проверяемый триплет.
    '''
    trpStr = str(trpStr);
    
    # Проверка префикса.
    i = 1;
    while ((trpStr[i] not in systemSymbols) and (trpStr[i] != " ")): i += 1;
    if (i == 1):
        if (trpStr[i] == trpPoint):
            return 3; # Ошибка: отсутствие префикса триплета.
    if (trpStr[i] == trpEqual):
        return 5; # Ошибка: не задано имя триплета.
    if (trpStr[i] != trpPoint):
        return 4; # Ошибка: некорректный префикс.

    # Проверка имени.
    i += 1;
    while ((trpStr[i] not in systemSymbols) and (trpStr[i] != " ")): i += 1;
    if (trpStr[i-1] == trpPoint):
        return 5; # Ошибка: не задано имя триплета.
    if (trpStr[i] == " "):
        while (trpStr[i] == " "): i += 1;
        if (trpStr[i] != trpEqual):
            return 6; # Ошибка: наличие недопустимых символов в имени триплета (или отсутствие знака присваивания).
    while (trpStr[i] not in systemSymbols): i += 1;
    if (trpStr[i] != trpEqual):
        return 6; # Ошибка: наличие недопустимых символов в имени триплета (или отсутствие знака присваивания).

    # Проверка значения.
    i += 1;
    while (trpStr[i] == " "): i += 1;
    value = "";
    if (trpStr[i] == trpAps): # Если триплет имеет строковое значение.
        i += 1;
        while ((trpStr[i] != trpAps) and (i != len(trpStr) - 1)):
            i += 1;
        if (i == len(trpStr) - 1):
            return 7; # Ошибка: отсутствие закрывающего апострофа в значении триплета.
        i += 1;
    else:
        if (trpStr[i] == trpRequest): # Если значение триплета представляет собой запрос.
            i += 1;
        else: # Если триплет имеет численное значение.
            while ((trpStr[i] != trpKv) and (i != len(trpStr) - 1)):
                value += trpStr[i];
                i += 1;
            try:
                value = float(value);
            except ValueError:
                return 8; # Ошибка: строковое значение триплета не обрамлено в апострофы.

    # Проверка комментария.
    if (i >= len(trpStr) - 2): return 0;

    while (trpStr[i] == " "): i += 1;
    if (trpStr[i] != trpKv and trpStr[i] != trpEnd): return 9; # Ошибка: наличие посторонних символов после значения триплета, не оформленных в комментарий.
    if (trpStr[-2] != trpKv): return 10; # Ошибка: отсутствие закрывающей кавычки в комментарии (или есть посторонние символы после комментария).
    if (trpStr[i+1:-2].count(trpKv) != 0): return 9; # Ошибка: наличие посторонних символов после значения триплета, не оформленных в комментарий.

    return 0;

def trpDel(trpStr, prefix, name):
    '''
    Удаляет все триплеты с заданными префиксом и именем из триплексной строки.

    Параметры:
        trpStr - триплексная строка;
        prefix - префикс, по которому производится удаление;
        name - имя, по которому при соответствующем префиксе производится удаление.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    triplets = trpSplit(trpStr);
    kolTrp = len(triplets);
    result = "";

    for i in range(kolTrp):
        if ((trpGetPrefix(triplets[i])[1] != prefix) or (trpGetName(triplets[i])[1] != name)): result += triplets[i];

    return (0, result);

def trpDelPref(trpStr, prefix):
    '''
    Удаляет все триплеты с заданным префиксом из триплексной строки.

    Параметры:
        trpStr - триплексная строка;
        prefix - префикс, по которому производится удаление.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    triplets = trpSplit(trpStr);
    kolTrp = len(triplets);
    result = "";

    for i in range(kolTrp):
        if (trpGetPrefix(triplets[i])[1] != prefix): result += triplets[i];

    return (0, result);

def trpGet(trpStr, prefix, name):
    '''
    Возвращает значение триплета с заданными префиксом и именем.

    Параметры:
        trpStr - строка, в которой производится поиск;
        prefix - префикс искомого триплета;
        name - имя искомого триплета.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    triplets = trpSplit(trpStr);
    kolTrp = len(triplets);

    for i in range(kolTrp):
        if ((trpGetPrefix(triplets[i])[1] == prefix) and (trpGetName(triplets[i])[1] == name)):
            return (0, trpGetValue(triplets[i])[1]);

    return (-1,);

def trpGetName(trpStr):
    '''
    Возвращает имя триплета в соответствии с синтаксисом:
    $<префикс>.<имя>=<значение>["Комментарий"];
    
    Параметры:
        trpStr - триплексная строка.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    result = trpStr[trpStr.index(trpPoint) + 1 : trpStr.index(trpEqual)];
    result = result.strip();
    return (0, result);

def trpGetPrefix(trpStr):
    '''
    Возвращает префикс триплета в соответствии с синтаксисом:
    $<префикс>.<имя>=<значение>["Комментарий"];
    
    Параметры:
        trpStr - триплексная строка.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    result = trpStr[trpStr.find(trpBeg) + 1 : trpStr.index(trpPoint)];
    return (0, result);

def trpGetValue(trpStr):
    '''
    Возвращает значение триплета в соответствии с синтаксисом:
    $<префикс>.<имя>=<значение>["Комментарий"];
    
    Параметры:
        trpStr - триплексная строка.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    result = trpStr[trpStr.index(trpEqual) + 1 : trpStr.find(trpKv)];
    result = result.strip();
    if (result[0] == trpAps): result = result[1 : -1];
    return (0, result);


def trpGoNext(trpStr, beginIndex):
    '''
    Возвращает индекс начала следующего триплета, осуществляя поиск с заданного индекса.
    
    Параметры:
        trpStr - триплексная строка;
        currentIndex - индекс, с которого нужно начинать поиск.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);

    index = beginIndex;
    lenStr = len(trpStr);
    
    while (index < lenStr and trpStr[index] != trpBeg): index += 1;

    return (0, index);

def trpMergeStr(trpStr, trpStrAdd):
    '''
    Сливает две триплексных строки. Возвращает результат слияния.
    
    Параметры:
        trpStr - основная триплексная строка;
        trpStrAdd - добавляемая триплексная строка.
    '''
    # Если исходные строки содержат ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0 or trpCheck(trpStrAdd) != 0):
        return (-1,);
    
    return (0, trpStr.strip() + trpStrAdd.strip());

def trpSort(trpStr):
    '''
    Cортирует триплексную строку в лексикографическом порядке имен. Возвращает отсортированную триплексную строку.

    Параметры:
        trpStr - триплексная строка.
    '''
    # Если исходная строка содержит ошибки, то функция прекращает свою работу.
    if (trpCheck(trpStr) != 0):
        return (-1,);
    
    triplets = trpSplit(trpStr);
    kolTrp = len(triplets);
    for i in range(kolTrp):
        triplets[i] = triplets[i][1:]; # Удаление символа $ в триплетах.

    triplets.sort(); # Сортировка строки.

    result = "";
    
    for i in range(kolTrp): # Генерация результирующей строки.
        result += trpBeg + str(triplets[i]);

    return (0, result);

def trpSplit(trpStr):
    '''
    Разбивает триплексную строку на триплеты. Возвращает список триплетов.

    Параметры:
        trpStr - триплексная строка.
    '''  
    arr = trpStr.split(trpEnd);
    kolTrp = len(arr); # Количество триплетов в исходной строке.
    
    for i in range(kolTrp):
        try:
            arr[i] = arr[i].strip();
            arr[i] = arr[i][1:];
        except IndexError:
            break;
        if (len(arr[i]) == 0):
            del arr[i];
        else:
            arr[i] = trpBeg + arr[i] + trpEnd;

    return arr;
