from django.template import Library

register = Library()


@register.filter(name='float_filter')
def float_filter(num):
    return str(num).replace(',', '.')


@register.filter(name='date_translate')
def date_translate(date):
    days = {'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда', 'Thursday': 'Четверг',
            'Friday': 'Пятница', 'Saturday': 'Суббота', 'Sunday': 'Воскресенье'}
    return days.get(date)
