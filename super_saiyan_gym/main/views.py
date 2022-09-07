from random import randint
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import TrainingProgram, Exercises, MyFavorites
from django.views.generic import DetailView, ListView, CreateView
from .forms import TrainingProgramForm


@login_required
def main(request):
    train_programs = TrainingProgram.objects.select_related('category').filter(is_published=True).all()
    count = train_programs.aggregate(count=Count('id'))['count']
    rand_trains = []
    if len(train_programs) >= 3:
        while len(rand_trains) != 3:
            rand_i = randint(0, count - 1)
            if train_programs[rand_i] not in rand_trains:
                rand_trains.append(train_programs[rand_i])
    context = {'train_programs': rand_trains}
    return render(request, 'main/main.html', context)


class TrainProgramDetail(DetailView):
    model = TrainingProgram
    template_name = 'main/program_detail.html'
    context_object_name = 'program'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return TrainingProgram.objects.filter(is_published=True).prefetch_related('exercises').all()

    def get_context_data(self, **kwargs):
        context = super(TrainProgramDetail, self).get_context_data(**kwargs)
        query = self.object.exercises.select_related('category').order_by('category').all()
        exercises = {item.category: [] for item in query}
        for exercise in query:
            exercises[exercise.category].append(exercise.title)
        context['exercises'] = exercises
        if self.request.user.training.all().exists():
            context['training'] = self.request.user.training.select_related('train_program').first()
        return context


class TrainProgramList(ListView):
    model = TrainingProgram
    template_name = 'main/programs_list.html'
    context_object_name = 'train_programs'
    login_url = reverse_lazy('login')
    paginate_by = 3

    def get_queryset(self):
        return TrainingProgram.objects.filter(is_published=True).select_related('category', 'author').prefetch_related('exercises').all()


class UserCreateTrainProgramView(CreateView):
    model = TrainingProgram
    success_url = reverse_lazy('after_create_user_program')
    login_url = reverse_lazy('login')
    template_name = 'main/program_user_create.html'
    form_class = TrainingProgramForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return render(self.request, 'main/after_create_user_program.html')


class ExercisesList(ListView):
    model = Exercises
    template_name = 'main/exercises_list.html'
    context_object_name = 'exercises'
    login_url = reverse_lazy('login')
    paginate_by = 10
    extra_context = {'backup_url': reverse_lazy('exercises_list')}

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return Exercises.objects.select_related('category').order_by(f"-{self.request.GET.get('filter_by')}").all()
        return Exercises.objects.select_related('category').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesList, self).get_context_data(**kwargs)
        if self.request.GET.get('filter_by'):
            context['cur_filter'] = self.request.GET.get('filter_by')
            context['url_arg_cur_filter'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class ExercisesSearchList(ListView):
    model = Exercises
    template_name = 'main/exercises_list.html'
    paginate_by = 10
    login_url = reverse_lazy('login')
    context_object_name = 'exercises'

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return Exercises.objects.select_related('category')\
                .filter(title__icontains=self.request.GET.get('search_word'))\
                .order_by(f"-{self.request.GET.get('filter_by')}").all()
        return Exercises.objects.select_related('category')\
            .filter(title__icontains=self.request.GET.get('search_word')).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesSearchList, self).get_context_data(**kwargs)
        context['search_word'] = self.request.GET.get('search_word')
        context['url_arg_cur_filter'] = f"&search_word={self.request.GET.get('search_word')}"
        if self.request.GET.get('filter_by'):
            context['backup_url'] = self.request.path
            context['cur_filter'] = self.request.GET.get('filter_by')
            context['url_arg_cur_filter'] += f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class ExercisesByCategoryList(ListView):
    model = Exercises
    template_name = 'main/exercises_by_category_list.html'
    context_object_name = 'exercises'
    login_url = reverse_lazy('login')
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return Exercises.objects.select_related('category').filter(category__title=self.kwargs.get('cat_title'))\
                .order_by(f"-{self.request.GET.get('filter_by')}").all()
        return Exercises.objects.select_related('category').filter(category__title=self.kwargs.get('cat_title')).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesByCategoryList, self).get_context_data(**kwargs)
        context['category_title'] = self.kwargs.get('cat_title')
        context['backup_url'] = self.request.path
        if self.request.GET.get('filter_by'):
            context['cur_filter'] = self.request.GET.get('filter_by')
            context['url_arg_cur_filter'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class ExercisesByCategorySearchList(ListView):
    model = Exercises
    template_name = 'main/exercises_by_category_list.html'
    paginate_by = 10
    login_url = reverse_lazy('login')
    context_object_name = 'exercises'

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return Exercises.objects.select_related('category')\
                .filter(Q(category__title=self.kwargs.get('cat_title'))
                        & Q(title__icontains=self.request.GET.get('search_word')))\
                .order_by(f"-{self.request.GET.get('filter_by')}").all()
        return Exercises.objects.select_related('category')\
            .filter(Q(category__title=self.kwargs.get('cat_title'))
                    & Q(title__icontains=self.request.GET.get('search_word'))).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesByCategorySearchList, self).get_context_data(**kwargs)
        context['search_word'] = self.request.GET.get('search_word')
        context['url_arg_cur_filter'] = f"&search_word={self.request.GET.get('search_word')}"
        context['category_title'] = self.kwargs.get('cat_title')
        if self.request.GET.get('filter_by'):
            context['backup_url'] = self.request.path
            context['cur_filter'] = self.request.GET.get('filter_by')
            context['url_arg_cur_filter'] += f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class ExercisesDetail(DetailView):
    model = Exercises
    template_name = 'main/exercises_detail.html'
    login_url = reverse_lazy('login')
    context_object_name = 'exercise'

    def get_queryset(self):
        return Exercises.objects.select_related('category').all()

    def get_context_data(self, **kwargs):
        context = super(ExercisesDetail, self).get_context_data(**kwargs)
        context['in_favorite'] = self.request.user.favorite.filter(exercise__pk=self.object.id).exists()
        context['backup_url'] = self.request.META.get('HTTP_REFERER')
        return context


def add_in_favorites(request, pk):
    exercise_obj = Exercises.objects.select_related('category').get(pk=pk)
    if request.user.favorite.filter(exercise__pk=pk).exists():
        query = request.user.favorite.get(exercise__pk=pk)
        query.delete()
        exercise_obj.like = F('like') - 1
    else:
        MyFavorites.objects.create(user=request.user, exercise=exercise_obj, category=exercise_obj.category.title)
        exercise_obj.like = F('like') + 1
    exercise_obj.save()
    exercise_obj.refresh_from_db()
    return redirect('exercises_detail', pk=pk)
