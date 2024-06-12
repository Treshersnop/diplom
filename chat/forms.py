from django import forms

from chat import models


class Message(forms.ModelForm):
    files = forms.FileField(required=False)

    class Meta:
        model = models.Message
        fields = (
            'description',
            'files',
        )
