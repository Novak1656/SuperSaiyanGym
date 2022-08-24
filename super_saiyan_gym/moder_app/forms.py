from django import forms
from main.models import TrainingProgram, ExercisesCategory, Exercises


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ExercisesCategory
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
