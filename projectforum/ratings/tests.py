from django.test import TestCase, Client
from django.contrib.auth.models import User
from projectforum.ratings.models import *
from projectforum.projects.models import Project

# Create your tests here.

class RatingsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@gmail.com", password="password")
        self.reviewer = User.objects.create_user(username="user2", email="user2@gmail.com", password="password")
        self.project1 = Project.objects.create(
            title = "Test Title 1",
            description = "Test Description 1",
            owner = self.user,
            payment = 1,
            amount = 1,
            status = 3,
        )

    """docstring for RatingsTest"""
    def test_ratings_can_be_created(self):
        rating1 = UserReview.objects.create(
            reviewer = self.reviewer,
            recipient = self.user,
            score = 5,
            comment = "nice",
            project = self.project1
        )
        self.assertEqual(rating1.comment, "nice")
        self.assertEqual(rating1.score, 5)

    def test_post_ratings(self):
        form_data = {
            'score': 5,
            'comment': "nice"
        }
        c = Client()
        c.login(username="user2", password="password")
        url = '/ratings/review/' + str(self.project1.id)
        project_url = 'http://testserver/project/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp['Location'], project_url)

    def test_not_logged_in(self):
        form_data = {
            'score': 5,
            'comment': "nice"
        }
        c = Client()
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp['Location'], "http://testserver/profile/login")

    def test_invalid_project(self):
        form_data = {
            'score': 5,
            'comment': "nice"
        }
        c = Client()
        url = '/ratings/review/' + str(2)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 404)
