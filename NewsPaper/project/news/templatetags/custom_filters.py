from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает,
# где именно их искать и фильтры потеряются

@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):  # проверяем, что value — это точно строка,
        # а arg — точно число, чтобы не возникло курьёзов
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')  #  в случае,
        # если кто-то неправильно воспользовался нашим тегом, выводим ошибку

@register.filter(name='censor')
def filter_message(message: str):
    variants = ['хуй',
       'пизда',
       'джигурда',
       'пиздеть',
       'пиздить',
       'отпиздить',
       'опиздюлить',
       'опиздюлиться',
       ]
    ln = len(variants)
    filtred_message = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in message:
        string += i
        string2 = string.lower()
        flag = 0
        for j in variants:
            if not string.lower() in j:
                flag += 1
            if string.lower() == j:
                filtred_message += pattern * len(string)
                flag -= 1
                string = ''
        if flag == ln:
            filtred_message += string
            string = ''
    if string.lower() != '' and string.lower() not in variants:
        filtred_message += string
    elif string.lower() != '':
        filtred_message += pattern * len(string)
    return filtred_message

@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)