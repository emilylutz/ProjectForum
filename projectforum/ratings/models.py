from django.db import models
from django.contrib.auth.models import User
from projectforum.projects.models import *


# Create your models here.


class UserReview(models.Model):
    """docstring for UserReview"""
    reviewer = models.ForeignKey(User, related_name="user_review")
    recipient = models.ForeignKey(User, related_name="reviewed_user")
    project = models.ForeignKey(Project)
    score = models.IntegerField()
    comment = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

