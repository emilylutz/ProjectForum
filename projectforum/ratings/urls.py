""" ProjectForum's project module URL Configuration """

from django.conf.urls import include, patterns, url

from projectforum.ratings.views import *

urlpatterns = [
    url(r'^review/(?P<id>\d+)$', make_review),
    url(r'^review/edit/(?P<reviewid>\d+)$', edit_review),
]
