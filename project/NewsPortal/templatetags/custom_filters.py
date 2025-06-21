from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = ['редиска', 'плохиш']
    result = value
    for word in bad_words:
        censored_word = word[0] + '*' * (len(word) - 1)
        result = result.replace(word, censored_word)
        result = result.replace(word.capitalize(), censored_word)
    return result
