from django.test import TestCase
from projectforum.projects.models import Project

class ProjectsTest(TestCase):
	#def setUp(self):
		# add any set-up code here

	def test_that_tests_work(self):
		print "test works"

	def test_projects_can_be_created(self):
		project1 = Project.objects.create(
			title = "Test Title",
			description = "Test Description",
		)
		self.assertEqual(project1.title, "Test Title")
		self.assertEqual(project1.description, "Test Description")
		print "projects can be created"

		fetched_projects = Project.objects.filter()
		self.assertEqual(1, len(fetched_projects))
		print "projects can be gotten"

# Create your tests here.
