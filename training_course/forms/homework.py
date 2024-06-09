from django import forms

from training_course import models


class CreateHomework(forms.ModelForm):
    files = forms.FileField(required=False)

    class Meta:
        model = models.Homework
        fields = ('description', 'files')


class UpdateHomework(forms.ModelForm):
    files = forms.FileField(required=False)

    class Meta:
        model = models.Homework
        fields = ('description', 'files')
