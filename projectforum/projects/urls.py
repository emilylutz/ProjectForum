""" ProjectForum's project module URL Configuration """

from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from .views import ProjectListView

urlpatterns = [
    url(r'^list/$',
        ProjectListView.as_view(),
        name='list'),
    #add more urls here
]
