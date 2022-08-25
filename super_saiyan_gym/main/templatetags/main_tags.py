from django import template
from django.db.models import Count
from ..models import ExercisesCategory

register = template.Library()


@register.inclusion_tag('main/category_list.html')
def get_category_list():
    category = ExercisesCategory.objects.annotate(cnt=Count('exercises')).all()
    return {'category_list': category}
