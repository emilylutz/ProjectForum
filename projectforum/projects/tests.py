import json

from django.test import TestCase, Client
from .models import Project
from django.contrib.auth.models import User
from projectforum.user_profiles.models import UserProfile

import project_filters
import test_create_projects


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

    def test_add_project_applicants(self):
        project1 = Project.objects.create(
            title = "Test Title 1",
            description = "Test Description 1",
            owner = self.user,
            payment = 1,
            amount = 1,
            status = 1,
        )
        allApplicants = project1.applicants.all()
        self.assertEqual(0, len(allApplicants))

        joe = User.objects.create_user(username='joe',
                                             email='joe@gmail.com',
                                             password='topsecret2')

        # Add applicant to project
        project1.applicants.add(joe)

        #check that applicant is in project's applicants
        fetched_project = Project.objects.filter()[0]
        all_applicants = fetched_project.applicants.all()
        self.assertEqual(1, len(all_applicants))
        self.assertEqual(joe, all_applicants[0])

        #check that project is in applicant's projects applied to
        fetched_joe = User.objects.get(id=joe.id)
        self.assertEqual(1, len(fetched_joe.projects_applied_to.all()))
        self.assertEqual(project1, fetched_joe.projects_applied_to.all()[0])

    def test_accept_applicant_onto_team(self):
        project1 = Project.objects.create(
            title = "Test Title 1",
            description = "Test Description 1",
            owner = self.user,
            payment = 1,
            amount = 1,
            status = 1,
        )

        joe = User.objects.create_user(username='joe',
                                             email='joe@gmail.com',
                                             password='topsecret2')

        # Check that you can't accept an applicant who isn't in applicants
        self.assertFalse(project1.accept_applicant(joe))

        # Add applicant to project
        project1.applicants.add(joe)

        # Check that project doesn't have any team members yet
        allTeamMembers = project1.team_members.all()
        self.assertEqual(0, len(allTeamMembers))

        # Check that accepting an applicant in applicants works
        self.assertTrue(project1.accept_applicant(joe))

        # check that applicant is in project's team members
        fetched_project = Project.objects.filter()[0]
        allTeamMembers = fetched_project.team_members.all()
        self.assertEqual(1, len(allTeamMembers))
        self.assertEqual(joe, allTeamMembers[0])

        #check that project is in applicant's current_projects
        fetched_joe = User.objects.get(id=joe.id)
        self.assertEqual(0, len(fetched_joe.projects_applied_to.all()))
        self.assertEqual(1, len(fetched_joe.current_projects.all()))
        self.assertEqual(project1, fetched_joe.current_projects.all()[0])

    def test_list_projects(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(order='title', salary='Lump Sum',
                            ascending=False, starting_from = 0, ending_at = 10)
        self.assertEqual(1, response.body.status)
        self.assertEqual('F', response.body.projects[0].title)
