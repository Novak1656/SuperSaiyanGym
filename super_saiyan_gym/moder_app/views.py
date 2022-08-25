from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import AccessMixin
from main.models import TrainingProgram, ExercisesCategory, Exercises
from .forms import CategoryForm, ProgramForm, ExerciseForm
from django.urls import reverse_lazy


@login_required
def index(request):
    if not request.user.is_staff:
        raise Http404
    context = {'program_list': TrainingProgram.objects.values('id', 'title').all(),
               'category_list': ExercisesCategory.objects.values('id', 'title').all(),
               'exercise_list': Exercises.objects.values('id', 'title').all()}
    return render(request, 'moder_app/index.html', context)


class ModerCreateProgramView(AccessMixin, CreateView):
    model = TrainingProgram
    form_class = ProgramForm
    template_name = 'moder_app/moder_create.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'тренировочной программы'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ModerCreateCategoryView(AccessMixin, CreateView):
    model = ExercisesCategory
    template_name = 'moder_app/moder_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'категории упражнений'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ModerCreateExerciseView(AccessMixin, CreateView):
    model = Exercises
    template_name = 'moder_app/moder_create.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'упражнения'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ModerUpdateProgram(AccessMixin, UpdateView):
    model = TrainingProgram
    template_name = 'moder_app/moder_update.html'
    form_class = ProgramForm
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'тренировочной программы'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerUpdateProgram, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


class ModerUpdateCategory(AccessMixin, UpdateView):
    model = ExercisesCategory
    template_name = 'moder_app/moder_update.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    form_class = CategoryForm
    extra_context = {'page_title': 'категории упражнений'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerUpdateCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerUpdateCategory, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


class ModerUpdateExercise(AccessMixin, UpdateView):
    model = Exercises
    template_name = 'moder_app/moder_update.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    form_class = ExerciseForm
    extra_context = {'page_title': 'упражнения'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerUpdateExercise, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerUpdateExercise, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


class ModerDeleteProgram(AccessMixin, DeleteView):
    model = TrainingProgram
    template_name = 'moder_app/moder_delete.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'тренировочной программы', 'mes_title': 'тренировочную программу'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerDeleteProgram, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerDeleteProgram, self).get_context_data(**kwargs)
        context['obj_title'] = self.object.title
        return context


class ModerDeleteCategory(AccessMixin, DeleteView):
    model = ExercisesCategory
    template_name = 'moder_app/moder_delete.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'категории упражнений', 'mes_title': 'категорию упражнений'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerDeleteCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerDeleteCategory, self).get_context_data(**kwargs)
        context['obj_title'] = self.object.title
        return context


class ModerDeleteExercise(AccessMixin, DeleteView):
    model = Exercises
    template_name = 'moder_app/moder_delete.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'упражнения', 'mes_title': 'упражнение'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerDeleteExercise, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerDeleteExercise, self).get_context_data(**kwargs)
        context['obj_title'] = self.object.title
        return context
