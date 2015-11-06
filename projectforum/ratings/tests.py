from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class RatingsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@gmail.com", password="password")
        self.reviewer = User.objects.create_user(username="user2", email="user2@gmail.com", password="password")

    """docstring for RatingsTest"""
    def test_ratings_can_be_created(self):
        rating1 = UserReview.objects.create(
            reviewer=self.reviewer,
            recipient=self.user,
            score=5
            comment="nice",
        )
        self.assertEqual(rating1.comment, "nice")
        self.assertEqual(rating1.score, 5)
        # pass
