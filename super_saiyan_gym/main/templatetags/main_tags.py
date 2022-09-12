from django import template
from django.db.models import Count
from ..models import ExercisesCategory, Exercises, ProgramCategory, TrainingProgram

register = template.Library()


@register.inclusion_tag('main/category_list.html')
def get_category_list():
    category = ExercisesCategory.objects.annotate(cnt=Count('exercises')).all()
    exercises_cnt = len(Exercises.objects.all())
    return {'category_list': category, 'ex_cnt': exercises_cnt}


@register.inclusion_tag('main/filter_list.html')
def get_filter_list(cur_filter=None, backup_url=None, search_word=None):
    context = {
        'filter_list': [('title', 'Title'), ('like', 'Popularity'), ('created_at', 'New')],
        'cur_filter': cur_filter,
        'backup_url': backup_url,
        'search_word': search_word
    }
    return context


@register.inclusion_tag('main/program_category_list.html')
def get_program_category_list():
    category = ProgramCategory.objects.annotate(cnt=Count('train_program')).filter(cnt__gt=0).order_by('-cnt').all()
    program_cnt = TrainingProgram.objects.filter(is_published=True).all().count()
    return {'category_list': category, 'program_cnt': program_cnt}


@register.inclusion_tag('main/program_filter_list.html')
def get_program_filter_list(cur_filter=None, backup_url=None, search_word=None):
    context = {
        'filter_list': [('title', 'Title'), ('popularity', 'Popularity'), ('author', 'Author'),
                        ('days_in_week', 'Training in week')],
        'cur_filter': cur_filter,
        'backup_url': backup_url,
        'search_word': search_word
    }
    return context
