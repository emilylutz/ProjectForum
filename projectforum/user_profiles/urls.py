""" ProjectForum's user_profiles module URL Configuration """

from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from projectforum.user_profiles.views import (
    ActivateView,
    ProfileEditView,
    ProfileView,
    RegisterView
)

urlpatterns = [
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='register_activate_done.html'),
        name='activate_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivateView.as_view(),
        name='activate'),

    url(r'^edit/(?P<username>\w+)/$',
        ProfileEditView.as_view(),
        name='edit'),

    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'logout.html'},
        name='logout'),

    url(r'^password_change/$', auth_views.password_change,
        {'template_name': 'password_change_form.html',
         'post_change_redirect': 'profile:password_change_done'},
        name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done,
        {'template_name': 'password_change_done.html'},
        name='password_change_done'),

    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'password_reset_form.html',
         'email_template_name': 'password_reset_email.html',
         'subject_template_name': 'password_reset_subject.txt',
         'post_reset_redirect': 'profile:password_reset_done'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'password_reset_done.html'},
        name='password_reset_done'),

    url(r'^register/$',
        RegisterView.as_view(),
        name='register'),
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='register_complete.html'),
        name='register_complete'),

    url((r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-'
         r'[0-9A-Za-z]{1,20})/$'),
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html',
         'post_reset_redirect': 'profile:password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^view/(?P<username>\w+)/$',
        ProfileView.as_view(),
        name='view'),
]
