import pymorphy3

from django import template

register = template.Library()

morph = pymorphy3.MorphAnalyzer()

d_1 = []

forbidden_words = ['астроном', 'гороскоп', 'дед', 'пиво', 'Телевизор', 'Мужчина', 'драка', 'водка', 'Гренландия']


@register.filter()
def censor(text):
    for i in forbidden_words:
        p = morph.parse(i.lower())
        for l in p:
            for k in l.lexeme:
                d_1.append(k[0])

    t = list(text.split())

    for i in t:
        if i.isalpha():
            if i.lower() in d_1:
                t[t.index(i)] = i.replace(i[0:len(i) - 2:1], '*' * len(i[0:len(i) - 2:1]))
        else:
            if i.lower()[1:len(i):1] in d_1:
                t[t.index(i)] = i[0] + i[1:len(i):1].replace(i[1:len(i) - 2:1], '*' * len(i[1:len(i) - 2:1]))
            if i.lower()[0:len(i) - 1:1] in d_1:
                t[t.index(i)] = i[1:len(i):1].replace(i[1:len(i) - 2:1], '*' * len(i[1:len(i) - 2:1]))

    return " ".join(t)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.filter()
def cut_names(i):
    return i[1]


@register.filter()
def cut_number(i):
    return i[0]
