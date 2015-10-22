from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing a user account and its profile.
    """
    required_css_class = 'required'

    class Meta:
        model = UserProfile
        exclude = ['user']


class RegisterForm(UserCreationForm):
    """
    Form for registering a new user account.
    """
    required_css_class = 'required'
    email = forms.EmailField(label='Email')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        model = get_user_model()
        if model.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use.")
        return self.cleaned_data['email']
