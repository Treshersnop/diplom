from typing import Any

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from training_course import models


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CreateLesson(forms.ModelForm):
    files = MultipleFileField(required=False)
    task_name = forms.CharField(required=False)
    task_description = forms.CharField(widget=forms.Textarea, required=False)
    task_files = MultipleFileField(required=False)

    class Meta:
        model = models.Lesson
        fields = ('description', 'files', 'link', 'name', 'task_description', 'task_files', 'task_name')


class UpdateLesson(forms.ModelForm):
    files = MultipleFileField(required=False)
    task_name = forms.CharField(required=False)
    task_description = forms.CharField(widget=forms.Textarea, required=False)
    task_files = MultipleFileField(required=False)

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
