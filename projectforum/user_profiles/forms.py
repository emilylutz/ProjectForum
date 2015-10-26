from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import UserProfile, TagsField


class UserNamesEditForm(forms.ModelForm):
    """
    Form for editing a user account's first_name and last_name fields
    """
    required_css_class = 'required'

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing a user account's profile.
    """
    required_css_class = 'required'

    skills = TagsField()

    class Meta:
        model = UserProfile
        exclude = ['user']

    def clean_skills(self):
        skills = self.cleaned_data.get("skills")
        raise ValidationError("Nope: " + str(skills))


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
