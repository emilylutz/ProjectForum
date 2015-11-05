""" ProjectForum URL Configuration """

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('projectforum.user_profiles.urls',
                              namespace="profile")),
    url(r'^project/', include('projectforum.projects.urls',
                              namespace="project")),
    url(r'^ratings/', include('projectforum.ratings.urls',
                              namespace="ratings")),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
]
