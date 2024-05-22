from django import forms

from training_course import models
from training_course.forms.lesson import MultipleFileField


class CreateHomework(forms.ModelForm):
    files = MultipleFileField(required=False)

    class Meta:
        model = models.Homework
        fields = ('description', 'files')


class UpdateHomework(forms.ModelForm):
    files = MultipleFileField(required=False)

    class Meta:
        model = models.Homework
        fields = ('description', 'files')
