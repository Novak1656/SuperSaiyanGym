import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Training, TrainingProgram, ExercisesCategory, Schedules, Achievements, Exercises, TrainingProcess, ExerciseLvlUp
from .forms import ScheduleForm, BaseArticleFormSet
from django.forms import formset_factory
from datetime import datetime, timedelta

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

7. Каждую неделю мета выполнено сбрасывается с расписаний

8. Хранить в лвл апе объект упражнения вместо ид
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
    today_schedule = Schedules.objects.select_related('training').prefetch_related('exercises').filter(
        Q(training__user=request.user) & Q(day=Schedules.DAYS[datetime.now().date().weekday()][0]) & Q(complete=False)).first()
    if not today_schedule:
        raise Http404()
    today_training = today_schedule.exercises.all().values_list('exercises__category', flat=True).distinct()
    categories = ExercisesCategory.objects.filter(id__in=today_training).values_list('title', flat=True)
    TrainingProcess.objects.create(user=request.user)
    request.session['categories_list'] = [title for title in categories]
    return render(request, 'training_app/start_training.html', {'categories': categories})


@login_required
def training_process_steps(request, category):
    if request.META['HTTP_REFERER'] != f"http://{request.META['HTTP_HOST']}/training/start/":
        raise Http404()
    achievements = request.user.achievements.select_related('exercise').prefetch_related('exercise__category').filter(
        exercise__category__title=category).all()
    categories_list = request.session.get('categories_list')
    categories_list.remove(category)
    print(categories_list)
    if request.method == 'POST':
        train_proc = TrainingProcess.objects.filter(user=request.user).first()
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                if float(value) < 0:
                    messages.error(request, 'Показатели выполнения упражнений должны быть положительными!')
                else:
                    achieve = achievements.get(pk=key.split('_')[1])
                    if achieve.achieve_param < float(value):
                        ExerciseLvlUp.objects.create(training_process=train_proc, exercise_id=achieve.exercise_id,
                                                     old_achieve_param=achieve.achieve_param, new_achieve_param=value)
        if len(categories_list) == 0:
            return redirect('training_process_finish')
        category = categories_list[0]
        request.session['categories_list'] = categories_list
        request.session.modified = True
        return redirect('in_training', category=category)
    context = {'achievements': achievements, 'category': category, 'category_list': categories_list}
    return render(request, 'training_app/in_training.html', context)


@login_required
def training_process_finish(request):
    training_proc = TrainingProcess.objects.prefetch_related('exerciselvlup').filter(user=request.user).first()
    if not training_proc:
        raise Http404()
    cur_time = timezone.localtime(timezone.now()).time()
    start_time = timezone.localtime(training_proc.started_at, pytz.timezone(settings.TIME_ZONE)).time()
    cur_strptime = datetime.strptime(f"{cur_time.hour}:{cur_time.minute}:{cur_time.second}", "%H:%M:%S")
    start_strptime = datetime.strptime(f"{start_time.hour}:{start_time.minute}:{start_time.second}", "%H:%M:%S")
    time_end = cur_strptime - start_strptime

    lvl_ups = training_proc.exerciselvlup.all()
    exercises = Exercises.objects.select_related('category').filter(id__in=lvl_ups.values_list('exercise_id'))
    # хранить ид тренировочного процесса в сессии
    results = [(exercises.get(pk=item.exercise_id), item.old_achieve_param, item.new_achieve_param) for item in lvl_ups]

    achievements = request.user.achievements.select_related('exercise').filter(exercise_id__in=lvl_ups.values_list('exercise_id')).all()
    for achieve in achievements:
        for item in lvl_ups:
            if item.exercise_id == achieve.exercise_id:
                achieve.achieve_param = item.new_achieve_param
                achieve.save()
                break
    schedules = Schedules.objects.select_related('training').filter(Q(training__user=request.user) & Q(day=Schedules.DAYS[datetime.now().date().weekday()][0])).first()
    schedules.complete = True
    schedules.save()
    context = {'time_end': time_end, 'exercises': exercises, 'lvl_ups': lvl_ups, 'results': results}
    return render(request, 'training_app/training_results.html', context)


@login_required
def update_schedule(request, pk):
    days = Schedules.objects.select_related('training').filter(Q(training__user=request.user) & ~Q(pk=pk)).values_list('day', flat=True).all()
    schedule = get_object_or_404(Schedules, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, instance=schedule)
        if request.POST.get('day') in days:
            messages.error(request, 'Выберите разные дни для тренировок!')
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.complete = False
            schedule.save()
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
            return redirect('dojo')
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
