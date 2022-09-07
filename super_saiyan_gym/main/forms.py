from django import forms
from .models import TrainingProgram, Exercises


class TrainingProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        exclude = ['id', 'slug', 'author', 'moderation', 'is_published', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'days_in_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'training_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'retry_exercises': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        exercises = forms.ModelMultipleChoiceField(queryset=Exercises.objects.select_related('category').all(),
                                                   widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
