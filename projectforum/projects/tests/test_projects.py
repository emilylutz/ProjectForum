from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

import json

from projectforum.projects.forms import *
from projectforum.projects.models import Project
import projectforum.projects.project_filters as project_filters

import test_create_projects


class ProjectsTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='jacob',
                                                        email='jacob@mail.com',
                                                        password='topsecret')

    def test_that_tests_work(self):
        pass

    ##############
    # Model tests
    ##############
    def test_projects_can_be_created(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        # projects can be created
        self.assertEqual(project1.title, "Test Title")
        self.assertEqual(project1.description, "Test Description")

        # projects can be gotten
        fetched_projects = Project.objects.filter()
        self.assertEqual(1, len(fetched_projects))
        self.assertEqual(fetched_projects[0].title, "Test Title")

    def test_project_to_string(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        self.assertEqual(project1.__str__(), "Project: {title: Test Title 1}")

    def test_add_project_applicants(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        allApplicants = project1.applicants.all()
        self.assertEqual(0, len(allApplicants))

        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')

        # Add applicant to project
        project1.applicants.add(joe)

        # check that applicant is in project's applicants
        fetched_project = Project.objects.filter()[0]
        all_applicants = fetched_project.applicants.all()
        self.assertEqual(1, len(all_applicants))
        self.assertEqual(joe, all_applicants[0])

        # check that project is in applicant's projects applied to
        fetched_joe = self.user_model.objects.get(id=joe.id)
        self.assertEqual(1, len(fetched_joe.projects_applied_to.all()))
        self.assertEqual(project1, fetched_joe.projects_applied_to.all()[0])

    def test_accept_applicant_onto_team(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
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

        # check that project is in applicant's current_projects
        fetched_joe = self.user_model.objects.get(id=joe.id)
        self.assertEqual(0, len(fetched_joe.projects_applied_to.all()))
        self.assertEqual(1, len(fetched_joe.current_projects.all()))
        self.assertEqual(project1, fetched_joe.current_projects.all()[0])

    def test_project_to_string(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        self.assertEqual(project1.__str__(), "Project: {title: Test Title 1}")

    #################
    # List Page Tests
    #################

    def test_list_page_exists(self):
        c = Client()
        resp = c.get('/project/list/')
        self.assertTrue(resp.is_rendered)
        self.assertEqual(0, len(resp.context_data['project_list']))

    def test_list_page_gets_projects_in_database(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        project2 = Project.objects.create(
            title="Test Title 2",
            description="Test Description 2",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        resp = c.get('/project/list/')

        resp_projects = resp.context_data['project_list']
        self.assertEqual(2, len(resp_projects))

    def test_list_page_gets_project_in_database(self):
        project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        resp = c.get('/project/list/')

        resp_projects = resp.context_data['project_list']
        self.assertEqual(project1, resp_projects[0])

    # Create Tests
    def test_valid_data(self):
        form_data = {
            'title': "project1",
            'description': "project description 1",
            'payment': 1,
            'amount': 1
        }
        project_form = ProjectForm(data=form_data)
        self.assertTrue(project_form.is_valid())

    def test_redirect(self):
        c = Client()
        resp = c.get("/project/create/")
        self.assertEqual(
            resp['Location'],
            'http://testserver/profile/login/?next=/project/create/'
        )

    def test_no_redirect(self):
        c = Client()
        c.login(username="jacob",
                password="topsecret",
                email="jacob@mail.com")
        resp = c.get("/project/create/")
        self.assertEqual(resp.status_code, 200)

    def test_list_projects_by_title_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='title',
                                                    salary='lump',
                                                    ascending=False)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('family guy', contents['projects'][0]['title'])
        self.assertEqual('Azrael', contents['projects'][-1]['title'])
        self.assertEqual('Cricket', contents['projects'][3]['title'])

    def test_list_projects_by_title_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('Azrael', contents['projects'][0]['title'])
        self.assertEqual('family guy', contents['projects'][-1]['title'])
        self.assertEqual('decoy', contents['projects'][3]['title'])

    def test_list_projects_by_newest(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='timestamp',
                                                    salary='lump',
                                                    ascending=False)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('fallen', contents['projects'][0]['title'])
        self.assertEqual('Barrel', contents['projects'][-1]['title'])
        self.assertEqual('Cricket', contents['projects'][3]['title'])

    def test_list_projects_by_oldest(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='timestamp',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('Barrel', contents['projects'][0]['title'])
        self.assertEqual('fallen', contents['projects'][-1]['title'])
        self.assertEqual('decoy', contents['projects'][3]['title'])

    def test_list_projects_by_pay_lump_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='payment',
                                                    salary='lump',
                                                    ascending=False)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('decoy', contents['projects'][0]['title'])
        self.assertEqual('Barrel', contents['projects'][-1]['title'])
        self.assertEqual('Cricket', contents['projects'][3]['title'])

    def test_list_projects_by_pay_lump_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='payment',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('Azrael', contents['projects'][0]['title'])
        self.assertEqual('Cricket', contents['projects'][-1]['title'])
        self.assertEqual('Barrel', contents['projects'][3]['title'])

    def test_list_projects_by_pay_hourly_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=False)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('Cricket', contents['projects'][0]['title'])
        self.assertEqual('Azrael', contents['projects'][-1]['title'])
        self.assertEqual('decoy', contents['projects'][3]['title'])

    def test_list_projects_by_pay_hourly_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('Barrel', contents['projects'][0]['title'])
        self.assertEqual('decoy', contents['projects'][-1]['title'])
        self.assertEqual('Azrael', contents['projects'][3]['title'])

    def test_list_projects_status(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=2,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('A2', contents['projects'][0]['title'])

        response = project_filters.get_project_list(status=3,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('A3', contents['projects'][0]['title'])

        response = project_filters.get_project_list(status=4,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual('A4', contents['projects'][0]['title'])

    def test_list_projects_error1(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='apples',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(-1, contents['status'])

    def test_list_projects_error2(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=100,
                                                    keywords='',
                                                    order='payment',
                                                    salary='hourly',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, contents['status'])
        self.assertEqual(0, len(contents['projects']))

    def test_list_projects_error3(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_project_list(status=1,
                                                    keywords='',
                                                    order='payment',
                                                    salary='apples',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(-1, contents['status'])
