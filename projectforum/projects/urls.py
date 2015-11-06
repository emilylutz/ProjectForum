""" ProjectForum's project module URL Configuration """

from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    url(r'^list/$',
        ProjectListView.as_view(),
        name='list'),
    url(r'^create/$',
        CreateView.as_view(),
        name='create'),
    url(r'^create/complete/$',
        TemplateView.as_view(template_name='create_success.html'),
        name='create_success'),
    url(r'^create/fail/$',
        TemplateView.as_view(template_name='create_fail.html'),
        name='create_fail'),
    url(r'^(?P<id>\d+)/$', ProjectDetailView.as_view()),
    url(r'^(?P<id>\d+)/accept_applicant/(?P<username>\w+)$', accept_applicant),
    url(r'^(?P<id>\d+)/apply/$', apply_to_project),
    url(r'^(?P<id>\d+)/withdraw_application/$', withdraw_application),
    url(r'^(?P<id>\d+)/mark_complete/$', mark_complete),
    url(r'^(?P<id>\d+)/cancel_project/$', cancel_project),
    url(r'^(?P<id>\d+)/reopen_project/$', reopen_project),
    url(r'^(?P<id>\d+)/reopen_applications/$', reopen_applications),
    url(r'^(?P<id>\d+)/close_applications/$', close_applications),
]
