from django import forms

from core import models


class CreateProfile(forms.ModelForm):
    is_staff = forms.BooleanField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'patronymic', 'birthday')


class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'patronymic', 'birthday', 'avatar')
