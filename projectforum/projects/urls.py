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
    #add more urls here
]
