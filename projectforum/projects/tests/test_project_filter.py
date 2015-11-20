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

    def test_description_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['alpha']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(3, len(contents['projects']))
        self.assertEqual('B', contents['projects'][0]['title'])

    def test_owner_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['Bobicus']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(2, len(contents['projects']))
        self.assertEqual('C', contents['projects'][0]['title'])

    def test_tags_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['iOS']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(2, len(contents['projects']))
        self.assertEqual('B', contents['projects'][0]['title'])

    def test_many_tags_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['ios', 'android']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, len(contents['projects']))
        self.assertEqual('B', contents['projects'][0]['title'])

    def test_crazy_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['Bobicus', 'android', 'sixth', 'E']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(1, len(contents['projects']))
        self.assertEqual('E', contents['projects'][0]['title'])

    def test_failure_filter(self):
        test_create_projects.create_many_projects()
        keywords = ['Bobicus', 'android', 'sixth', 'seventh']
        response = project_filters.get_project_list(status=1,
                                                    keywords=keywords,
                                                    order='title',
                                                    salary='lump',
                                                    ascending=True)
        contents = json.loads(response.content)
        self.assertEqual(0, len(contents['projects']))
