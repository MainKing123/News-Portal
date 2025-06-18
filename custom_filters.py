from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='censor')
def censor(value):
    """
    Цензурирует нежелательные слова в строке.
    """
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам.")

    bad_words = ['редиска', 'плохиш']  
    result = value

    for word in bad_words:
        censored_word = word[0] + '*' * (len(word) - 1)  # Заменяем все буквы, кроме первой, звездочками
        result = result.replace(word, censored_word)
        result = result.replace(word.capitalize(), censored_word)  # Учитываем слова, начинающиеся с заглавной буквы

    return result


@register.filter(name='censor_safe')
def censor_safe(value):
 
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам.")

    bad_words = ['редиска', 'плохиш']  
    result = conditional_escape(value) 

    for word in bad_words:
        censored_word = word[0] + '*' * (len(word) - 1)  # Заменяем все буквы, кроме первой, звездочками
        result = result.replace(word, censored_word)
        result = result.replace(word.capitalize(), censored_word) # учитываем заглавные буквы

    return mark_safe(result) # помечаем как безопасный.
