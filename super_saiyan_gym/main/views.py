from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import TrainingProgram, Exercises, ExercisesCategory
from django.views.generic import DetailView, ListView


@login_required
def main(request):
    train_programs = TrainingProgram.objects.all()[:3]
    context = {'train_programs': train_programs}
    return render(request, 'main/main.html', context)


class TrainProgramDetail(DetailView):
    model = TrainingProgram
    template_name = 'main/program_detail.html'
    context_object_name = 'program'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return TrainingProgram.objects.prefetch_related('exercises').all()

    def get_context_data(self, **kwargs):
        context = super(TrainProgramDetail, self).get_context_data(**kwargs)
        query = self.object.exercises.select_related('category').order_by('category').all()
        exercises = {item.category: [] for item in query}
        for exercise in query:
            exercises[exercise.category].append(exercise.title)
        context['exercises'] = exercises
        return context


class TrainProgramList(ListView):
    model = TrainingProgram
    template_name = 'main/programs_list.html'
    context_object_name = 'train_programs'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return TrainingProgram.objects.prefetch_related('exercises').all()


def start_training(request):
    user = request.user
    user.train_program = TrainingProgram.objects.get(slug=request.GET.get('slug'))
    user.save()
    return redirect('profile')


def end_training(request):
    if request.user.train_program:
        user = request.user
        user.train_program = None
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


class ExercisesList(ListView):
    model = Exercises
    template_name = 'main/exercises_list.html'
    context_object_name = 'exercises'
    login_url = reverse_lazy('login')
    paginate_by = 10

    def get_queryset(self):
        return Exercises.objects.select_related('category').all()


class ExercisesByCategoryList(ListView):
    model = Exercises
    template_name = 'main/exercises_by_category_list.html'
    context_object_name = 'exercises'
    login_url = reverse_lazy('login')
    paginate_by = 10

    def get_queryset(self):
        return Exercises.objects.select_related('category').filter(category__title=self.kwargs.get('cat_title')).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesByCategoryList, self).get_context_data(**kwargs)
        context['category_title'] = self.kwargs.get('cat_title')
        return context


class ExercisesDetail(DetailView):
    model = Exercises
    template_name = 'main/exercises_detail.html'
    login_url = reverse_lazy('login')
    context_object_name = 'exercise'

    def get_queryset(self):
        return Exercises.objects.select_related('category').all()
