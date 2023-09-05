from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

from portfolio.account.models import Profile

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    consent = forms.BooleanField(
        help_text=mark_safe('Agree with our <a href="#">terms and conditions</a>.'),
        label='',
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'consent')
        error_messages = {
            'username': {
                'unique': 'This username is already taken',
            },
            'email': {
                'unique': 'User with this email already exists'
            },
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }


class AppUserDeleteForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance
