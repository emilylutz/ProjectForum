from django.contrib.auth.models import User
from django.test import TestCase, Client

import json

from projectforum.projects.models import Project
from projectforum.ratings.models import UserReview


class RatingsTest(TestCase):

    def setUp(self):
        self.recipient = User.objects.create_user(username="user1",
                                                  email="user1@gmail.com",
                                                  password="password")
        self.reviewer = User.objects.create_user(username="user2",
                                                 email="user2@gmail.com",
                                                 password="password")
        self.project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.recipient,
            payment=1,
            amount=1,
            status=3,
        )

        self.project1.team_members.add(self.recipient)
        self.project1.team_members.add(self.reviewer)
        self.project1.save()

    def test_ratings_can_be_created(self):
        rating1 = UserReview.objects.create(
            reviewer=self.reviewer,
            recipient=self.recipient,
            score=5,
            comment="ratings can be created",
            project=self.project1
        )
        self.assertEqual(rating1.comment, "ratings can be created")
        self.assertEqual(rating1.score, 5)

    def test_post_ratings(self):
        form_data = {
            'score': 5,
            'comment': "test post ratings",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        url = '/ratings/review/' + str(self.project1.id)
        project_url = 'http://testserver/project/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp['Location'], project_url)

    def test_not_logged_in(self):
        form_data = {
            'score': 5,
            'comment': "test nog logged in",
            'recipient_username': self.reviewer.username,
        }
        c = Client()
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp['Location'], "http://testserver/profile/login")

    def test_invalid_project(self):
        form_data = {
            'score': 5,
            'comment': "test invalid project",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        url = '/ratings/review/' + str(9999999)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 404)

    # test error when person tries to rate another >1 times on the same project
    def test_post_multiple_ratings(self):
        form_data = {
            'score': 5,
            'comment': "nice",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        c.login(username="user2", password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        reviews = UserReview.objects.filter(
            reviewer=self.reviewer, recipient=self.recipient, project=self.project1)
        self.assertEqual(len(reviews), 1)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 409)

    def test_edit_rating(self):
        form_data = {
            'score': 5,
            'comment': "test edit rating",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        c.login(username="user2", password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        review = UserReview.objects.get(
            reviewer=self.reviewer, recipient=self.recipient, project=self.project1)
        self.assertEqual(review.score, 5)
        self.assertEqual(review.comment, "test edit rating")
        new_data = {
            'score': 1,
            'comment': "new comment",
        }
        edit_url = '/ratings/review/edit/' + str(review.id)
        resp = c.post(edit_url, data=new_data)
        review = UserReview.objects.get(
            reviewer=self.reviewer, recipient=self.recipient, project=self.project1)
        self.assertEqual(review.score, 1)
        self.assertEqual(review.comment, "new comment")

    def test_edit_invalid_rating(self):
        c = Client()
        c.login(username="user2", password="password")
        edit_url = '/ratings/review/edit/429'
        resp = c.post(edit_url, data={})
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)

    def test_not_member_receive(self):
        user3 = User.objects.create_user(username="user3",
                                         email="user3@gmail.com",
                                         password="password")
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        form_data = {
            'score': 5,
            'comment': "test recipient is not part of project",
            'recipient_username': user3.username,
        }
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 403)

    def test_not_member_review(self):
        user3 = User.objects.create_user(username="user3",
                                         email="user3@gmail.com",
                                         password="password")
        c = Client()
        c.login(username=user3.username, password="password")
        form_data = {
            'score': 5,
            'comment': "test reviewer is not part of project",
            'recipient_username': self.recipient.username,
        }
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 403)

    def test_rate_self(self):
        form_data = {
            'score': 5,
            'comment': "test reviewer is not part of project",
            'recipient_username': self.reviewer.username,
        }
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 403)

    def test_open_project(self):
        self.project1 = Project.objects.create(
            title="Test Title 1",
            description="Test Description 1",
            owner=self.recipient,
            payment=1,
            amount=1,
            status=2,
        )
        form_data = {
            'score': 5,
            'comment': "test project is still in progress",
            'recipient_username': self.reviewer.username,
        }
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        self.assertEqual(resp.status_code, 403)

    def test_edit_different_review(self):
        form_data = {
            'score': 5,
            'comment': "test edit rating",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        review = UserReview.objects.get(
            reviewer=self.reviewer, recipient=self.recipient, project=self.project1)
        self.assertEqual(review.score, 5)
        self.assertEqual(review.comment, "test edit rating")
        edit_url = '/ratings/review/edit/' + str(review.id)
        c.login(username=self.recipient.username, password="password")
        resp = c.post(edit_url, data=form_data)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(data['errors'][0], 'User cannot edit another review')

    def test_edit_unauthorized(self):
        form_data = {
            'score': 5,
            'comment': "test edit rating",
            'recipient_username': self.recipient.username,
        }
        c = Client()
        c.login(username=self.reviewer.username, password="password")
        url = '/ratings/review/' + str(self.project1.id)
        resp = c.post(url, data=form_data)
        review = UserReview.objects.get(
            reviewer=self.reviewer, recipient=self.recipient, project=self.project1)
        self.assertEqual(review.score, 5)
        self.assertEqual(review.comment, "test edit rating")
        c = Client()
        edit_url = '/ratings/review/edit/' + str(review.id)
        resp = c.post(edit_url, data=form_data)
        data = json.loads(resp.content)
        self.assertEqual(data['status'], -1)
        self.assertEqual(data['errors'][0], 'User must login to edit review')
