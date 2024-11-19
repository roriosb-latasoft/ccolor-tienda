from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except TypeError:
        return 0  # Manejar errores de tipo si los valores no son numéricos

@register.filter
def sum_total(cart_items, field):
    try:
        return sum(item[field] * item['quantity'] for item in cart_items)
    except KeyError:
        return 0  # Manejar errores de campo si falta alguna clave
