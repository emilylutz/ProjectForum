from django.contrib.auth.models import User
from django.db import models


class ProjectTag(models.Model):
    """
    The projects can be tagged with descriptive text.
    """
    max_length = 100
    text = models.CharField(max_length=max_length)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'project tag'
        verbose_name_plural = 'project tags'

    def __str__(self):
        return "Project tag %s" % self.text


class Project(models.Model):

    PAYMENT_CHOICES = (
        (1, "Lump Sum"),
        (2, "Hourly"),
    )

    STATUSES = (
        (1, 'Accepting Applicants'),
        (2, 'In Progress'),
        (3, 'Canceled'),
        (4, 'Finished'),
    )

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    owner = models.ForeignKey(User)
    payment = models.IntegerField(choices=PAYMENT_CHOICES)
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUSES, default=1)
    tags = models.ManyToManyField(ProjectTag, related_name='projects',
                                  blank=True)
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
