from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    """
    Цензурирует нежелательные слова в строке.
    """
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам.")

    bad_words = ['редиска', 'плохиш']  # Добавьте сюда свой список "плохих" слов.  Учитывайте регистр!
    result = value

    for word in bad_words:
        censored_word = word[0] + '*' * (len(word) - 1)  # Заменяем все буквы, кроме первой, звездочками
        result = result.replace(word, censored_word)
        result = result.replace(word.capitalize(), censored_word)  # Учитываем слова, начинающиеся с заглавной буквы

    return result
