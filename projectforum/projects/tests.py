from django.test import TestCase, Client
from .models import Project
from django.contrib.auth.models import User


class ProjectsTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='jacob',
                                             email='jacob@gmail.com',
                                             password='topsecret')

	def test_that_tests_work(self):
		pass

	def test_projects_can_be_created(self):
		project1 = Project.objects.create(
			title = "Test Title",
			description = "Test Description",
			owner = self.user,
			payment = 1,
			amount = 1,
			status = 1,
		)

		# projects can be created
		self.assertEqual(project1.title, "Test Title")
		self.assertEqual(project1.description, "Test Description")

		# projects can be gotten
		fetched_projects = Project.objects.filter()
		self.assertEqual(1, len(fetched_projects))
		self.assertEqual(fetched_projects[0].title, "Test Title")

	def test_list_page_exists(self):
		c = Client()
		resp = c.get('/project/list/')
		self.assertTrue(resp.is_rendered)
		self.assertEqual(0, len(resp.context_data['project_list']))

	def test_list_page_gets_projects_in_database(self):
		project1 = Project.objects.create(
			title = "Test Title 1",
			description = "Test Description 1",
			owner = self.user,
			payment = 1,
			amount = 1,
			status = 1,
		)
		project2 = Project.objects.create(
			title = "Test Title 2",
			description = "Test Description 2",
			owner = self.user,
			payment = 1,
			amount = 1,
			status = 1,
		)
		c = Client()
		resp = c.get('/project/list/')

		resp_projects = resp.context_data['project_list']
		self.assertEqual(2, len(resp_projects))

	def test_list_page_gets_projects_in_database(self):
		project1 = Project.objects.create(
			title = "Test Title 1",
			description = "Test Description 1",
			owner = self.user,
			payment = 1,
			amount = 1,
			status = 1,
		)
		c = Client()
		resp = c.get('/project/list/')

		resp_projects = resp.context_data['project_list']
		self.assertEqual(project1, resp_projects[0])

	def test_project_to_string(self):
		project1 = Project.objects.create(
			title = "Test Title 1",
			description = "Test Description 1",
			owner = self.user,
			payment = 1,
			amount = 1,
			status = 1,
		)
		self.assertEqual(project1.__str__(), "Project: {title: Test Title 1}")
