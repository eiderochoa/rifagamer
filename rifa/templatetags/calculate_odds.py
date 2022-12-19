from django import template
register = template.Library()

@register.filter(name='calculate')
def calculate(value, num):
    return int(value) * int(num) + int(num)