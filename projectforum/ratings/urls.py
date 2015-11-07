""" ProjectForum's project module URL Configuration """

from django.conf.urls import include, patterns, url

from .views import *

urlpatterns = [
    url(r'^review/(?P<id>\d+)$', make_review)
]
