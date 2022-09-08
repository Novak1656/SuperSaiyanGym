from django.template import Library

register = Library()


@register.filter(name='sex_translate')
def sex_translate(sex):
    return {'Man': 'Мужской', 'Woman': 'Женский'}.get(sex)
