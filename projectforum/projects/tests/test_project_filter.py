from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

import json

from projectforum.projects.forms import *
from projectforum.projects.models import Project
import projectforum.projects.project_filters as project_filters

import test_create_projects


class ProjectsTest(TestCase):
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
        self.assertEqual('Barrel', contents['projects'][0]['title'])

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
        self.assertEqual('Cricket', contents['projects'][0]['title'])

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
        self.assertEqual('Barrel', contents['projects'][0]['title'])

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
        self.assertEqual('Barrel', contents['projects'][0]['title'])

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
        self.assertEqual('fallen', contents['projects'][0]['title'])

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

    def test_list_projects_by_title_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='title',
                                                salary='lump',
                                                ascending=False)
        contents = response
        self.assertEqual('family guy', contents[0].title)
        self.assertEqual('Azrael', contents[5].title)
        self.assertEqual('Cricket', contents[3].title)

    def test_list_projects_by_title_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='title',
                                                salary='lump',
                                                ascending=True)
        contents = response
        self.assertEqual('Azrael', contents[0].title)
        self.assertEqual('family guy', contents[5].title)
        self.assertEqual('decoy', contents[3].title)

    def test_list_projects_by_newest(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='timestamp',
                                                salary='lump',
                                                ascending=False)
        contents = response
        self.assertEqual('fallen', contents[0].title)
        self.assertEqual('Barrel', contents[5].title)
        self.assertEqual('Cricket', contents[3].title)

    def test_list_projects_by_oldest(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='timestamp',
                                                salary='lump',
                                                ascending=True)
        contents = response
        self.assertEqual('Barrel', contents[0].title)
        self.assertEqual('fallen', contents[5].title)
        self.assertEqual('decoy', contents[3].title)

    def test_list_projects_by_pay_lump_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='payment',
                                                salary='lump',
                                                ascending=False)
        contents = response
        self.assertEqual('decoy', contents[0].title)
        self.assertEqual('Barrel', contents[5].title)
        self.assertEqual('Cricket', contents[3].title)

    def test_list_projects_by_pay_lump_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='payment',
                                                salary='lump',
                                                ascending=True)
        contents = response
        self.assertEqual('Azrael', contents[0].title)
        self.assertEqual('Cricket', contents[5].title)
        self.assertEqual('Barrel', contents[3].title)

    def test_list_projects_by_pay_hourly_down(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='payment',
                                                salary='hourly',
                                                ascending=False)
        contents = response
        self.assertEqual('Cricket', contents[0].title)
        self.assertEqual('Azrael', contents[5].title)
        self.assertEqual('decoy', contents[3].title)

    def test_list_projects_by_pay_hourly_up(self):
        test_create_projects.create_many_projects()
        response = project_filters.get_projects(status=1,
                                                keywords='',
                                                order='payment',
                                                salary='hourly',
                                                ascending=True)
        contents = response
        self.assertEqual('Barrel', contents[0].title)
        self.assertEqual('decoy', contents[5].title)
        self.assertEqual('Azrael', contents[3].title)
