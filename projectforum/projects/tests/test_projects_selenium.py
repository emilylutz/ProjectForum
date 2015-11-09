from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from projectforum.projects.models import Project


class ProjectsSeleniumTest(TestCase):
    def setUp(self):
        settings.DEBUG = True
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='jacob',
                                                        email='jacob@mail.com',
                                                        password='topsecret')

    def test_that_tests_work(self):
        pass
