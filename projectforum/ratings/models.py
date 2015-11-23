from django.contrib.auth.models import User
from django.db import models

from projectforum.projects.models import *


class UserReview(models.Model):
    """ A review of a User by a User. """
    reviewer = models.ForeignKey(User, related_name="user_review")
    recipient = models.ForeignKey(User, related_name="reviewed_user")
    project = models.ForeignKey(Project)
    score = models.IntegerField()
    comment = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return "User review by %s" % self.reviewer
