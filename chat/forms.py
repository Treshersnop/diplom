from django import forms

from chat import models
from training_course.forms import MultipleFileField


class Message(forms.ModelForm):
    files = MultipleFileField(required=False)

    class Meta:
        model = models.Message
        fields = ('description', 'files',)
        widgets = {
            'description': forms.Textarea(attrs={'id': 'comment-field', 'rows': 4}),
        }
