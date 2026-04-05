from django import template
from json import loads
from random import shuffle



register = template.Library()

@register.filter
def range_num(n):
    return range(int(n))

# ------------------ Custom Filters ------------------

@register.filter
def space_to_value(text, replacement="_"):
    """
    Replace spaces in a string with a specified character (default "_").
    Usage in template: {{ "Hello World"|space_to_value:"-" }} -> Hello-World
    """
    if not text:
        return ""
    return text.replace(" ", replacement)

@register.filter
def initials(text):
    """
    Return initials of each word in the string.
    Usage in template: {{ "John Doe"|get_initials }} -> JD
    """
    if not text:
        return ""
    words = text.split()
    return "".join(word[0].upper() for word in words)


@register.filter
def firstPrice(text):
    price = loads(text)
    return price[0]


@register.filter
def shuffleInstances(instances):
    result = list(instances)
    shuffle(result)
    # print("Shuffled")
    return result
    