from typing import Any

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile

from training_course import models


class CreateLesson(forms.ModelForm):
    files = forms.FileField(required=False)
    task_name = forms.CharField(required=False)
    task_description = forms.CharField(widget=forms.Textarea, required=False)
    task_files = forms.FileField(required=False)

    class Meta:
        model = models.Lesson
        fields = ('description', 'files', 'link', 'name', 'task_description', 'task_files', 'task_name')


class UpdateLesson(forms.ModelForm):
    files = forms.FileField(required=False)
    task_name = forms.CharField(required=False)
    task_description = forms.CharField(widget=forms.Textarea, required=False)
    task_files = forms.FileField(required=False)

    class Meta:
        model = models.Lesson
        fields = ('description', 'files', 'link', 'name', 'task_description', 'task_files', 'task_name')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        lesson = kwargs['instance']

        try:
            task = lesson.task
            self.fields['task_name'].initial = task.name
            self.fields['task_description'].initital = task.description
            self.fields['task_files'].initial = task.files.all()

        except ObjectDoesNotExist:
            pass
