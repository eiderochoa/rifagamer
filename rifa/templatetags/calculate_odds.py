from django import template
register = template.Library()

@register.filter(name='calculate')
def calculate(value, num):
    return int(value) * int(num) + int(num)

@register.simple_tag
def percent(price,percent,num):
    total = float(price) * int(num)
    r_percent = (total * float(percent)) / 100
    return int(r_percent)


