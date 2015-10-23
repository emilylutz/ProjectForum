from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView

from .forms import ProfileEditForm, RegisterForm, UserNamesEditForm
from .models import RegistrationLink, UserProfile


class ActivateView(TemplateView):
    """
    User activation view.
    """
    template_name = 'register_activate.html'
    success_url = 'profile:activate_complete'

    def get(self, request, *args, **kwargs):
        if RegistrationLink.objects.activate_by_key(*args, **kwargs):
            return redirect(self.success_url)
        return super(ActivateView, self).get(request, *args, **kwargs)


class ProfileEditView(UpdateView):
    """
    User profile edit view.
    """
    template_name = 'edit.html'
    form_class = ProfileEditForm
    model = UserProfile

    def get(self, request, *args, **kwargs):
        self.profile_username = kwargs['username']
        self.profile = self.get_profile()
        if not self.profile:
            return redirect(self.get_success_url())
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.profile_username = kwargs['username']
        self.profile = self.get_profile()
        if not self.profile:
            return redirect(self.get_success_url())
        return super(ProfileEditView, self).post(request, *args, **kwargs)

    def get_object(self):
        return self.profile

    def get_profile(self):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=self.profile_username)
            user_profile = UserProfile.objects.get_or_create_profile(user)
            requester = self.request.user
            if not requester.is_authenticated() or (user.pk != requester.pk):
                user_profile = None
        except UserModel.DoesNotExist:
            user_profile = None
        return user_profile

    def get_success_url(self):
        return reverse('profile:view',
                       kwargs={'username':self.profile_username})

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context['user_form'] = UserNamesEditForm({
            'first_name': self.profile.user.first_name,
            'last_name': self.profile.user.last_name
        })
        return context

    def form_valid(self, form):
        user_form = UserNamesEditForm(**self.get_form_kwargs())
        if user_form.is_valid():
            self.profile.user.first_name = user_form.cleaned_data['first_name']
            self.profile.user.last_name = user_form.cleaned_data['last_name']
            self.profile.user.save()
            return super(ProfileEditView, self).form_valid(form)
        else:
            return super(ProfileEditView, self).form_invalid(form)

    def form_invalid(self, form):
        user_form = UserNamesEditForm(**self.get_form_kwargs())
        user_form.is_valid()
        return super(ProfileEditView, self).form_invalid(form)


class ProfileView(TemplateView):
    """
    User profile view.
    """
    template_name = 'view.html'

    def get(self, request, *args, **kwargs):
        UserModel = get_user_model()
        self.can_edit = False
        try:
            user = UserModel.objects.get(username=kwargs['username'])
            self.user_profile = UserProfile.objects.get_or_create_profile(user)
            if request.user.is_authenticated():
                self.can_edit = (user.pk == request.user.pk)
        except UserModel.DoesNotExist:
            self.user_profile = None
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'can_edit': self.can_edit,
            'user_profile': self.user_profile
        })
        return context


class RegisterView(FormView):
    """
    User registration views.
    """
    template_name = 'register_form.html'
    form_class = RegisterForm
    success_url = 'profile:register_complete'

    def form_valid(self, form):
        site = get_current_site(self.request)
        model = get_user_model()

        data = form.cleaned_data
        new_user = model.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password1'),
        )
        registration_link = RegistrationLink.objects.create_inactive_user(
            site, new_user, self.request)

        return redirect(self.success_url)
