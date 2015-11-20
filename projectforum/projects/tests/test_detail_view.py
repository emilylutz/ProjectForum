from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

import json

from projectforum.projects.models import Project


class ProjectsDetailViewTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='jacob',
                                                        email='jacob@mail.com',
                                                        password='topsecret')

    # Helper functions
    def basicDetailViewTests(self, resp, project):
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(project, resp.context['project'])
        self.assertTemplateUsed(resp, 'project_detail.html')
        self.assertContains(resp, project.title, 1)
        self.assertContains(resp, project.description, 1)
        self.assertContains(resp, project.get_status_display(), 1)

    def test_project_detail_view_exists(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/')
        self.assertTrue(resp.is_rendered)

    def test_project_detail_view_gets_correct_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/')
        self.assertEqual(project1, resp.context['project'])

    def test_project_detail_view_error_when_project_doesnt_exist(self):
        c = Client()
        resp = c.get('/project/37/')
        self.assertEqual(404, resp.status_code)

    def test_project_detail_view_correct_context_when_user_not_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/')
        self.basicDetailViewTests(resp, project1)

        # User specific tests
        self.assertNotContains(resp, 'apply_button')
        self.assertContains(resp, 'Log in to apply')
        self.assertNotContains(resp, 'applicant_list')
        self.assertNotContains(resp, 'member_list')
        self.assertNotContains(resp, 'owner_list')
        self.assertNotContains(resp, 'reviewing your application')

    def test_project_detail_view_correct_context_when_owner_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/')
        self.basicDetailViewTests(resp, project1)

        self.assertTrue(resp.context['logged_in'])
        self.assertEqual(self.user, resp.context['user'])

        # User specific tests
        self.assertNotContains(resp, 'apply_button')
        self.assertNotContains(resp, 'Log in to apply')
        self.assertContains(resp, 'applicant_list')
        self.assertContains(resp, 'member_list')
        self.assertNotContains(resp, 'owner_list')
        self.assertNotContains(resp, 'reviewing your application')
        # TODO: test that owner can see button for accepting applicants
        # TODO: test that owner can cancel the project or mark it as complete
        # TODO: maybe test specific cases for if there are applicants or team
        #       members vs not.

    def test_project_detail_view_context_when_other_user_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/')
        self.basicDetailViewTests(resp, project1)

        self.assertTrue(resp.context['logged_in'])
        self.assertEqual(joe, resp.context['user'])

        # User specific tests
        self.assertContains(resp, 'apply_button')
        self.assertNotContains(resp, 'Log in to apply')
        self.assertNotContains(resp, 'applicant_list')
        self.assertNotContains(resp, 'member_list')
        self.assertNotContains(resp, 'owner_list')
        self.assertNotContains(resp, 'reviewing your application')

    def test_project_detail_view_context_when_applied_user_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/')
        self.basicDetailViewTests(resp, project1)

        self.assertTrue(resp.context['logged_in'])
        self.assertEqual(joe, resp.context['user'])

        # User specific tests
        self.assertNotContains(resp, 'apply_button')
        self.assertNotContains(resp, 'Log in to apply')
        self.assertNotContains(resp, 'applicant_list')
        self.assertNotContains(resp, 'member_list')
        self.assertNotContains(resp, 'owner_list')
        self.assertContains(resp, 'reviewing your application')

    def test_project_detail_view_context_when_team_member_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)
        project1.accept_applicant(joe)

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/')
        self.basicDetailViewTests(resp, project1)

        self.assertTrue(resp.context['logged_in'])
        self.assertEqual(project1, resp.context['project'])
        self.assertEqual(joe, resp.context['user'])

        # User specific tests
        self.assertNotContains(resp, 'apply_button')
        self.assertNotContains(resp, 'Log in to apply')
        self.assertNotContains(resp, 'applicant_list')
        self.assertContains(resp, 'member_list')
        self.assertContains(resp, 'owner_list')
        self.assertNotContains(resp, 'reviewing your application')

    # Accepting Applicant tests

    def test_owner_accepting_applicant(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/accept_applicant/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        self.assertEqual(0, len(project1.applicants.all()))
        self.assertEqual(project1.team_members.all()[0], joe)

    def test_non_owner_accepting_applicant(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/accept_applicant/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.team_members.all()))
        self.assertEqual(project1.applicants.all()[0], joe)

    def test_not_logged_in_accepting_applicant(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/accept_applicant/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.team_members.all()))
        self.assertEqual(project1.applicants.all()[0], joe)

    def test_owner_accepting_applicant_on_invalid_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) +
                     '/accept_applicant/' + joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.team_members.all()))
        self.assertEqual(project1.applicants.all()[0], joe)

    def test_owner_accepting_invalid_applicant(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/accept_applicant/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.team_members.all()))
        self.assertEqual(0, len(project1.applicants.all()))


    # Test removing a team member
    def test_owner_removing_team_member(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.team_members.add(joe)

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/remove_team_member/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        self.assertEqual(0, len(project1.team_members.all()))

    def test_team_member_removing_self(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.team_members.add(joe)

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/remove_team_member/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        self.assertEqual(len(project1.team_members.all()), 0)

    def test_non_owner_removing_team_member(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        steve = self.user_model.objects.create_user(username='steve',
                                                  email='steve@mail.com',
                                                  password='topsecret3')
        project1.team_members.add(joe)

        c = Client()
        self.assertTrue(c.login(username=steve.username, password='topsecret3'))
        resp = c.get('/project/' + str(project1.id) + '/remove_team_member/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(project1.team_members.all()[0], joe)

    def test_not_logged_in_removing_team_member(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.team_members.add(joe)

        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/remove_team_member/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(project1.team_members.all()[0], joe)

    def test_owner_removing_team_member_on_invalid_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.team_members.add(joe)

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) +
                     '/remove_team_member/' + joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(project1.team_members.all()[0], joe)

    def test_owner_removing_team_member_invalid_applicant(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/accept_applicant/' +
                     joe.username)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)

    # Test applying to projects
    def test_applying(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/apply/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        self.assertEqual(project1.applicants.all()[0], joe)

    def test_applying_not_logged_in(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/apply/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.applicants.all()))

    def test_applying_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))

        resp = c.get('/project/' + str(project1.id+1) + '/apply/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(0, len(project1.applicants.all()))

    # Withdrawing Application tests
    def test_applicant_withdrawing_application(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/withdraw_application/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        self.assertEqual(0, len(project1.applicants.all()))
        self.assertEqual(0, len(project1.team_members.all()))

    def test_non_applicant_withdrawing_application(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)
        john = self.user_model.objects.create_user(username='john',
                                                   email='john@mail.com',
                                                   password='topsecret3')

        c = Client()
        self.assertTrue(c.login(username=john.username, password='topsecret3'))
        resp = c.get('/project/' + str(project1.id) + '/withdraw_application/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(1, len(project1.applicants.all()))

    def test_non_logged_in_withdrawing_application(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        resp = c.get('/project/' + str(project1.id) + '/withdraw_application/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(1, len(project1.applicants.all()))

    def test_withdrawing_application_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) +
                     '/withdraw_application/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(1, len(project1.applicants.all()))

    # mark complete tests
    def test_owner_marking_project_as_complete(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/mark_complete/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(4, project1.status)

    def test_non_owner_marking_project_as_complete(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        project1.applicants.add(joe)

        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/mark_complete/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    def test_owner_marking_bad_project_as_complete(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) + '/mark_complete/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    # test cancel project

    def test_owner_canceling_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/cancel_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(3, project1.status)

    def test_non_owner_canceling_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/cancel_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    def test_owner_canceling_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) + '/cancel_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    # Testing reopening project
    def test_reopening_after_marked_as_complete(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=4,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/reopen_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(2, project1.status)

    def test_reopening_after_canceling(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=3,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/reopen_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(2, project1.status)

    def test_non_owner_reopening(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=4,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/reopen_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    def test_reopening_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=4,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) + '/reopen_project/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    # testing reopening applications
    def test_reopening_applications(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=2,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/reopen_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(1, project1.status)

    def test_reopening_applications_non_owner(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=2,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username,
                                password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/reopen_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    def test_reopening_applications_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=2,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) +
                     '/reopen_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project1.status, project.status)

    # testing close applications
    def test_closing_applications(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )

        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id) + '/close_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], 1)
        project1 = Project.objects.get(id=project1.id)
        self.assertEqual(2, project1.status)

    def test_closing_applications_non_owner(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=joe.username, password='topsecret2'))
        resp = c.get('/project/' + str(project1.id) + '/close_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project.status, project1.status)

    def test_closing_applications_bad_project(self):
        project1 = Project.objects.create(
            title="Test Title",
            description="Test Description",
            owner=self.user,
            payment=1,
            amount=1,
            status=1,
        )
        joe = self.user_model.objects.create_user(username='joe',
                                                  email='joe@mail.com',
                                                  password='topsecret2')
        c = Client()
        self.assertTrue(c.login(username=self.user.username,
                                password='topsecret'))
        resp = c.get('/project/' + str(project1.id + 1) +
                     '/close_applications/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        project = Project.objects.get(id=project1.id)
        self.assertEqual(project.status, project1.status)

    # Test project page when project is in different states: cancelled,
    # completed, in progress, accepting applicants
