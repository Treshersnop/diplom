from django import forms

from training_course import models


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CreateTask(forms.ModelForm):
    files = MultipleFileField(required=False)

    class Meta:
        model = models.Task
        fields = ('description', 'files', 'name')


class CreateLesson(forms.ModelForm):
    files = MultipleFileField(required=False)
    task_name = forms.CharField(required=False)
    task_description = forms.CharField(widget=forms.Textarea, required=False)
    task_files = MultipleFileField(required=False)

    class Meta:
        model = models.Lesson
        fields = ('description', 'files', 'link', 'name', 'task_description', 'task_files', 'task_name')


class UpdateLesson(forms.ModelForm):
    # files = forms.FileField(
    #     label='Файлы',
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #     required=False
    # )

    class Meta:
        model = models.TrainingCourse
        fields = ('name',)
