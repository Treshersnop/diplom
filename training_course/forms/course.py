from django import forms

from training_course import models


class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.TrainingCourse
        fields = (
            'category',
            'description',
            'from_data',
            'image',
            'level',
            'name',
            'responsible',
            'to_data',
        )


class UpdateCourse(forms.ModelForm):
    class Meta:
        model = models.TrainingCourse
        fields = (
            'category',
            'description',
            'from_data',
            'image',
            'level',
            'name',
            'to_data',
        )
