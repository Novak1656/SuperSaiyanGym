from django import forms
from django.core.exceptions import ValidationError
from .models import Schedules, ExercisesCategory


class BaseArticleFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        days = []
        for form in self.forms:
            if form.cleaned_data.get('day') in days:
                raise ValidationError('Выберите разные дни для тренировок!')
            days.append(form.cleaned_data.get('day'))


class ScheduleForm(forms.ModelForm):
    def __init__(self, exercises_list, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['exercises'].queryset = exercises_list

    class Meta:
        model = Schedules
        fields = ('day', 'exercises',)
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'})
        }
        exercises = forms.ModelMultipleChoiceField(
            queryset=ExercisesCategory.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})
        )

