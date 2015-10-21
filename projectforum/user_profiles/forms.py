from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    """
    Form for registering a new user account.
    """
    required_css_class = 'required'
    email = forms.EmailField(label='Email')

    class Meta:
        model = get_user_model()
        fields = (getattr(model, 'USERNAME_FIELD', 'username'), 'email')
