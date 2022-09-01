from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Training, TrainingProgram, ExercisesCategory, Schedules, Achievements, Exercises, TrainingProcess, ExerciseLvlUp
from .forms import ScheduleForm, BaseArticleFormSet, AchievementsForm
from django.forms import formset_factory
from datetime import datetime

"""
1.Начать тренировку
после выполнения отображаемого упражнения нажимается кнопка далее и отображается следующее упражнение
время начала и конца тренировки запоминается и в кноце выводится результат
+Создать модель БД в которую будут заносится промежуточные данные во время тренировки:
- время начала и конца тренеровки
- упражнения параметры достижений, которых были увеличены в ходе тренировки

2.В профиле добавить разделы:
+-общие достижения
-список программ по которым проходили тренировки (дата начала тренировок по программе и дата конца)

3.Реализовать функцию подбора программы по следующим параметрам: рост, вес, возраст
Добавить программам категорию: похудение, набор массы, стандартный, фитнес

4.Реализовать возможность пользователям создавать кастомные программы

5. Добавить в модель Расписание поле выполнено.

6. В разделе сегодняшняя тренеровка если она выполнена то выводить результаты тренеровки, результаты сохраняются 1 день.
"""


def mailing():
    users_trains = Training.objects.prefetch_related('schedules').select_related('user').filter(mailing=True).all()
    mail_list = []
    for train in users_trains:
        schedule = train.schedules.prefetch_related('exercises').filter(day=Schedules.DAYS[datetime.now().date().weekday()][0]).first()
        if schedule:
            message = f"Сегодня у вас тренировка на следующие группы мышц: {', '.join([exercise.title for exercise in schedule.exercises.all()])}."
            mail_list += ('Не пропустите сегодняшнюю тренировку!', message, settings.EMAIL_HOST_USER, [train.user.email]),
    send_mass_mail(mail_list, fail_silently=False)
    print("Рассылка выполнена")


@login_required
def dojo(request):
    context = dict()
    context['training'] = TrainingProgram.objects.prefetch_related('training').filter(
        training__user=request.user).values_list('exercises', flat=True).all()
    context['exercises'] = Exercises.objects.select_related('category').filter(id__in=context.get('training')).all()
    context['schedules'] = Schedules.objects.prefetch_related('exercises').select_related('training').filter(
        training__user=request.user).all()
    context['today_training'] = context.get('schedules').filter(
        day=Schedules.DAYS[datetime.now().date().weekday()][0]).first()
    context['achievements'] = Achievements.objects.select_related('exercise').prefetch_related('exercise__category')\
        .filter(Q(user=request.user) & Q(exercise__id__in=context.get('training'))).all()
    cat_id_list = context.get('exercises').values_list('category', flat=True).distinct()
    context['categories'] = ExercisesCategory.objects.filter(id__in=cat_id_list).values_list('title', flat=True).all()
    return render(request, 'training_app/main.html', context)


@login_required
def training_process_start(request):
    today_training = Schedules.objects.select_related('training').prefetch_related('exercises').filter(
        Q(training__user=request.user) & Q(day=Schedules.DAYS[datetime.now().date().weekday()][0])).first().\
        exercises.all().values_list('exercises__category', flat=True).distinct()
    categories = ExercisesCategory.objects.filter(id__in=today_training).values_list('title', flat=True)
    TrainingProcess.objects.create(user=request.user)
    return render(request, 'training_app/start_training.html', {'categories': categories})


@login_required
def training_process_steps(request, category):
    query = request.user.achievements.select_related('exercise').prefetch_related('exercise__category').filter(
        exercise__category__title=category).all()
    AchievementsFormSet = formset_factory(AchievementsForm, extra=len(query), max_num=len(query))
    if request.method == 'POST':
        formset = AchievementsFormSet(request.POST, queryset=query)
        print(formset)
        if formset.is_valid():
            for form in formset:
                achieve = form(instance=Achievements.objects.get(form.cleaned_data['id']))
                print(achieve)
                # if achieve.achieve_param < form.cleaned_data['achieve_param']:
                #     ExerciseLvlUp.objects.create()
                # achieve.achieve_param =
                #return redirect('in_training', category=category)
    else:
        formset = AchievementsFormSet(initial=[{'achieve_param': item.achieve_param} for item in query])
    exercises = [(i + 1, item.exercise, item.achieve_param) for i, item in enumerate(query)]
    context = {'exercises': exercises, 'category': category, 'category_list': '', 'formset': formset}
    return render(request, 'training_app/in_training.html', context)


@login_required
def training_process_finish(request):
    return render(request, 'training_app/in_training.html')


@login_required
def update_schedule(request, pk):
    days = Schedules.objects.select_related('training').filter(Q(training__user=request.user) & ~Q(pk=pk)).values_list('day', flat=True).all()
    schedule = get_object_or_404(Schedules, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, instance=schedule)
        if request.POST.get('day') in days:
            messages.error(request, 'Выберите разные дни для тренировок!')
        if form.is_valid():
            form.save()
            return redirect('dojo')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'training_app/update_schedule.html', {'form': form})


@login_required
def training_conf(request):
    if Schedules.objects.select_related('training').filter(training__user=request.user).exists():
        raise Http404()
    query = TrainingProgram.objects.prefetch_related("training", "exercises").filter(
        training__user=request.user).values_list('exercises__category', 'days_in_week').distinct()
    exercises_list = ExercisesCategory.objects.filter(id__in=[item[0] for item in query])
    ScheduleFormSet = formset_factory(ScheduleForm, extra=query[0][1], formset=BaseArticleFormSet)
    if request.method == 'POST':
        formset = ScheduleFormSet(request.POST, form_kwargs={'exercises_list': exercises_list})
        if formset.is_valid():
            for form in formset:
                schedule = form.save(commit=False)
                schedule.training = Training.objects.filter(user=request.user).first()
                schedule.save()
                form.save_m2m()
            return redirect('profile')
    else:
        formset = ScheduleFormSet(form_kwargs={'exercises_list': exercises_list})
    return render(request, 'training_app/training_conf.html', {'formset': formset})


@login_required
def create_training(request):
    training_program = TrainingProgram.objects.prefetch_related('exercises').get(slug=request.GET.get('slug'))
    Training.objects.create(user=request.user, train_program=training_program)
    exercises = training_program.exercises.all()
    for exercise in exercises:
        if not Achievements.objects.filter(user=request.user, exercise=exercise).exists():
            Achievements.objects.create(user=request.user, exercise=exercise)
    return redirect('training_conf')


@login_required
def delete_training(request):
    if request.user.training:
        Training.objects.filter(user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def start_mailing(request):
    train = request.user.training.first()
    if train.mailing:
        train.mailing = False
        train.save()
        return redirect('dojo')
    train.mailing = True
    train.save()
    return redirect('dojo')
