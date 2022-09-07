from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from main.models import TrainingProgram, ExercisesCategory, Exercises, ProgramCategory
from django.core.mail import send_mail


class ProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        fields = ('title', 'description', 'days_in_week', 'training_count', 'retry_exercises', 'exercises', 'category',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'days_in_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'training_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'retry_exercises': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        exercises = forms.ModelMultipleChoiceField(
            queryset=Exercises.objects.select_related('category').all(),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})
        )

    def __init__(self, *args, **kwargs):
        self.moder = kwargs.pop('moder')
        super(ProgramForm, self).__init__(*args, **kwargs)

    def save(self):
        program = super(ProgramForm, self).save(commit=False)
        if not program.is_published:
            program.is_published = True
            send_mail('Ваша тренеровочная программа опубликована!',
                      f"Тренеровочная программа {program.title.upper()},"
                      f" опубликованная вами {program.created_at.strftime('%d.%m.%Y в %H:%M:%S')}"
                      f" упешно прошла модерацию и была добавлена в список наших тренеровочных программ.\n\n"
                      f"http://127.0.0.1:8000{reverse_lazy('program_detail', kwargs={'slug': program.slug})}\n\n"
                      f" Спасибо за вашу активность!", settings.EMAIL_HOST_USER, [program.author.email])
        program.moderation = self.moder
        program.save()
        return program


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ExercisesCategory
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercises
        fields = ('title', 'category',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProgramCategoryForm(forms.ModelForm):
    class Meta:
        model = ProgramCategory
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
