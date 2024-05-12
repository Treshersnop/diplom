from django import forms

from training_course import models


class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.TrainingCourse
        exclude = ('is_active', 'number_of_clicks', 'cost', 'sale')
