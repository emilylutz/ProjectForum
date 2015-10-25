from django.db import models
from django.contrib.auth.models import User


#title, description, owner, team, status, tags
class Project(models.Model):

    PAYMENT_CHOICES = (
        (1, "Lump sum"),
        (2, "Hourly"),
    )

    STATUSES = (
        (1, "In progress"),
        (2, 'Canceled'),
        (3, 'Finished'),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey(User)
    #team = models.ManyToManyField(User)
    payment = models.IntegerField(choices=PAYMENT_CHOICES)
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUSES, default=1)
    tags = models.CharField(max_length=2048, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "Project: {title: "+self.title+"}"