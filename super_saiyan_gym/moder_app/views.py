from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import AccessMixin
from main.models import TrainingProgram, ExercisesCategory, Exercises, ProgramCategory
from .forms import CategoryForm, ProgramForm, ExerciseForm, ProgramCategoryForm
from django.urls import reverse_lazy


@login_required
def index(request):
    if not request.user.is_staff:
        raise Http404
    context = {'program_list': TrainingProgram.objects.filter(is_published=True).values('id', 'title').all(),
               'category_list': ExercisesCategory.objects.values('id', 'title').all(),
               'exercise_list': Exercises.objects.values('id', 'title').all(),
               'program_category_list': ProgramCategory.objects.values('id', 'title').all(),
               'train_suggests': TrainingProgram.objects.select_related('author').filter(is_published=False).all()
               }
    return render(request, 'moder_app/index.html', context)


@login_required
def get_suggestion(request, slug):
    if not request.user.is_staff:
        raise Http404
    suggest = TrainingProgram.objects.get(slug=slug)
    if request.method == 'POST':
        form = ProgramForm(moder=request.user.username, data=request.POST, instance=suggest)
        if form.is_valid():
            form.save()
            return redirect('moder')
    else:
        form = ProgramForm(moder=request.user.username, instance=suggest)
    return render(request, 'moder_app/suggestion.html', {'form': form, 'suggestion_title': suggest.title, 'slug': slug})


@login_required
def delete_suggestion(request, slug):
    if not request.user.is_staff:
        raise Http404
    t_program = TrainingProgram.objects.select_related('author').get(slug=slug)
    send_mail('Ваша тренеровочная программа отклонена!',
              f"Тренеровочная программа {t_program.title.upper()},"
              f" опубликованная вами {t_program.created_at.strftime('%d.%m.%Y в %H:%M:%S')}"
              f" не прошла модерацию и была оклонена.\n\n"
              f" Вы можете попробовать заново предложить свою программу тренировок!",
              settings.EMAIL_HOST_USER, [t_program.author.email])
    t_program.delete()
    return redirect('moder')


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'moder': self.request.user.username})
        return kwargs


class ModerCreateCategoryView(AccessMixin, CreateView):
    model = ExercisesCategory
    template_name = 'moder_app/moder_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('exercises_list')
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
    success_url = reverse_lazy('exercises_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'упражнения'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ModerCreateProgramCategoryView(AccessMixin, CreateView):
    model = ProgramCategory
    template_name = 'moder_app/moder_create.html'
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'категории тренировочной программы'}
    form_class = ProgramCategoryForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerCreateProgramCategoryView, self).dispatch(request, *args, **kwargs)


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'moder': self.request.user.username})
        return kwargs


class ModerUpdateCategory(AccessMixin, UpdateView):
    model = ExercisesCategory
    template_name = 'moder_app/moder_update.html'
    success_url = reverse_lazy('exercises_list')
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
    success_url = reverse_lazy('exercises_list')
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


class ModerUpdateProgramCategory(AccessMixin, UpdateView):
    model = ProgramCategory
    success_url = reverse_lazy('program_list')
    login_url = reverse_lazy('login')
    template_name = 'moder_app/moder_update.html'
    extra_context = {'page_title': 'категории тренировочной программы'}
    form_class = ProgramCategoryForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        super(ModerUpdateProgramCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerUpdateProgramCategory, self).get_context_data(**kwargs)
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


class ModerDeleteProgramCategory(AccessMixin, DeleteView):
    model = ProgramCategory
    success_url = reverse_lazy('program_list')
    template_name = 'moder_app/moder_delete.html'
    login_url = reverse_lazy('login')
    extra_context = {'page_title': 'категории тренировочной программы',
                     'mes_title': 'категории тренировочной программы'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ModerDeleteProgramCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerDeleteProgramCategory, self).get_context_data(**kwargs)
        context['obj_title'] = self.object.title
        return context
