from django import forms
from main.models import TrainingProgram, ExercisesCategory, Exercises, ProgramCategory


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
        program.is_published = True
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
