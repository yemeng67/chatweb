from django import template

register = template.Library()

@register.filter(name='split')
def split_filter(value, arg):
    """自定义字符串分割过滤器"""
    return value.split(arg) if arg else []