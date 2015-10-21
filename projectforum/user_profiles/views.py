from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .forms import RegisterForm

class RegisterView(FormView):
    """
    Base class for user registration views.
    """
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = 'profile:registration_complete'

    def form_valid(self, request, form):
        new_user = self.register(request, form)
        return redirect(success_url)

    def register(self, request, form):
        """
        Implement user-registration logic here. Access to both the
        request and the full cleaned_data of the registration form is
        available here.
        """
        raise None
