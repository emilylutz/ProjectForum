from django.test import TestCase, Client
from projectforum.projects.models import Project
from django.contrib.auth.models import User
from django.conf import settings


class ProjectsSeleniumTest(TestCase):
	def setUp(self):
		settings.DEBUG = True
		self.user = User.objects.create_user(username='jacob',
                                             email='jacob@gmail.com',
                                             password='topsecret')

	def test_that_tests_work(self):
		pass