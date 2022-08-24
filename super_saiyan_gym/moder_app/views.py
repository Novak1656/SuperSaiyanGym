from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import AccessMixin
from main.models import TrainingProgram, ExercisesCategory, Exercises
from .forms import CategoryForm
from django.urls import reverse_lazy


def index(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            raise Http404
    return render(request, 'moder_app/index.html')


class ModerCreateView(AccessMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('create_target') == 'program':
            self.form_class = ''
            return TrainingProgram.objects.all()
        elif self.request.GET.get('create_target') == 'category':
            self.form_class = CategoryForm
            return ExercisesCategory.objects.all()
        elif self.request.GET.get('create_target') == 'exercise':
            self.form_class = ''
            return Exercises.objects.all()
    template_name = 'moder_app/moder_create.html'
    success_url = reverse_lazy('programs_list')
