from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

import json

from projectforum.projects.forms import *
from projectforum.projects.models import Project, ProjectApplication
import projectforum.projects.project_filters as project_filters

import test_create_projects


class ProjectsApplicationsTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.jacob = self.user_model.objects.create_user(username='jacob',
                                                         email='j@mail.com',
                                                         password='secret')
        self.project = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.jacob,
            payment=1,
            amount=1,
            status=1,
        )
        self.joe = self.user_model.objects.create_user(username='joe',
                                                       email='joe@mail.com',
                                                       password='topsecret2')
        self.steve = self.user_model.objects.create_user(username='steve',
                                                         email='s@mail.com',
                                                         password='topsecret3')

    def test_project_applications(self):
        joe_application = ProjectApplication.objects.create(
            applicant=self.joe,
            project=self.project,
            text='I am joe'
        )
        steve_application = ProjectApplication.objects.create(
            applicant=self.steve,
            project=self.project,
            text='I am steve'
        )

        self.assertIn(joe_application, self.project.applications.all())
        self.assertIn(steve_application, self.project.applications.all())

        self.assertIn(joe_application, self.joe.applications.all())
        self.assertIn(steve_application, self.steve.applications.all())
