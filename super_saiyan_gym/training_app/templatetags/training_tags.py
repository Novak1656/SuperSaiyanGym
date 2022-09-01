from django.template import Library

register = Library()


def float_filter(num):
    return str(num).replace(',', '.')


register.filter('float_filter', float_filter)
