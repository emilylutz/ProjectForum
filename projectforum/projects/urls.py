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
    #add more urls here
]
