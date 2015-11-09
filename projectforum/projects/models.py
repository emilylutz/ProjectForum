from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):

    PAYMENT_CHOICES = (
        (1, "Lump sum"),
        (2, "Hourly"),
    )

    STATUSES = (
        (1, 'Accepting Applicants'),
        (2, 'In progress'),
        (3, 'Canceled'),
        (4, 'Finished'),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey(User)
    payment = models.IntegerField(choices=PAYMENT_CHOICES)
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUSES, default=1)
    tags = models.CharField(max_length=2048, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    team_members = models.ManyToManyField(User,
                                          related_name="current_projects",
                                          blank=True)
    applicants = models.ManyToManyField(User,
                                        related_name="projects_applied_to",
                                        blank=True)

    def accept_applicant(self, applicant):
        if applicant in self.applicants.all():
            self.applicants.remove(applicant)
            self.team_members.add(applicant)
            return True
        else:
            return False

    def __str__(self):
        return "Project: {title: "+self.title+"}"
