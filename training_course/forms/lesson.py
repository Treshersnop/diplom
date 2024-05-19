from django import forms

from training_course import models


class CreateLesson(forms.ModelForm):
    class Meta:
        model = models.Lesson
        fields = ('name', 'description', 'link')


class UpdateLesson(forms.ModelForm):
    class Meta:
        model = models.TrainingCourse
        exclude = ('is_active', 'number_of_clicks', 'responsible')