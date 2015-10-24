from django.test import TestCase
from django.contrib.auth.models import User

class UserProfilesTest(TestCase):
	#def setUp(self):
		# add any set-up code here

	def test_create_user(self):
		user = User.objects.create_user(username='jacob', email='jacob@gmail.com', password='topsecret')
		self.assertEqual(user.username, "jacob")
		fetched_users = User.objects.filter()
		self.assertEqual(1, len(fetched_users))



# Create your tests here.
