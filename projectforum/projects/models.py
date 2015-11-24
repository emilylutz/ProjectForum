from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class ProjectTag(models.Model):
    """
    The projects can be tagged with descriptive text.
    """
    max_length = 100
    text = models.CharField(max_length=max_length)

    class Meta:
        verbose_name = 'project tag'
        verbose_name_plural = 'project tags'

    def __unicode__(self):
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
    amount = models.IntegerField(validators=[MinValueValidator(0, message="Please enter a positive amount")])
    status = models.IntegerField(choices=STATUSES, default=1)
    tags = models.ManyToManyField(ProjectTag, related_name='projects',
                                  blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    team_members = models.ManyToManyField(User,
                                          related_name="current_projects",
                                          blank=True)

    def accept_application(self, applicant):
        application = self.application_given_applicant(applicant)
        if application is not None:
            application.delete()
            self.team_members.add(application.applicant)
            return True
        else:
            return False

    def remove_application(self, applicant):
        application = self.application_given_applicant(applicant)
        if application is not None:
            application.delete()
            return True
        else:
            return False

    def applicants(self):
        applicants = []
        for application in self.applications.all():
            applicants += [application.applicant]
        return applicants

    def application_given_applicant(self, applicant):
        for application in self.applications.all():
            if application.applicant == applicant:
                return application
        return None

    def __unicode__(self):
        return "Project: {title: "+self.title+"}"


class ProjectApplication(models.Model):
    """
    Applications to project.
    """
    applicant = models.ForeignKey(User,
                                  related_name="applications")
    project = models.ForeignKey(Project,
                                related_name="applications")
    text = models.TextField(max_length=2048)

    # def __unicode__(self):
    #     return self.applicant.username + ', ' + self.text

    class Meta:
        verbose_name = 'project application'
        verbose_name_plural = 'project applications'

    def __unicode__(self):
        key = self.applicant.username + ", " + self.project.title
        return "Project Application %s" % key
