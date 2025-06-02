
from django import template

register = template.Library()

@register.filter(name='mayusculas')
def mayusculas(valor):
    """Convierte el texto a mayúsculas"""
    return str(valor).upper()

@register.filter(name='truncar')
def truncar(valor, longitud=50):
    """Trunca un texto a una longitud específica"""
    valor = str(valor)
    if len(valor) > longitud:
        return valor[:longitud] + "..."
    return valor
