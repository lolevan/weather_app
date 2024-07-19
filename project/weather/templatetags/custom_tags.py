from django import template

register = template.Library()


@register.filter
def zip_lists(a, b):
    # Объединяет два списка, создавая список кортежей, где каждый кортеж состоит из элементов обоих списков с одинаковыми индексами.
    return zip(a, b)
