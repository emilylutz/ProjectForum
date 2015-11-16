from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, Client

from projectforum.user_profiles.models import UserProfile


class UserProfilesTest(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        self.assertEqual(user.username, "jacob")
        fetched_users = self.user_model.objects.filter()
        self.assertEqual(1, len(fetched_users))

    def test_manual_authentication_success(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        auth_test = authenticate(username='jacob', password='topsecret')
        self.assertNotEqual(auth_test, None)
        self.assertTrue(auth_test.is_active)

    def test_manual_authentication_fail_wrong_password(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        auth_test = authenticate(username='jacob', password='wrongsecret')
        self.assertEqual(auth_test, None)

    def test_manual_authentication_fail_wrong_username(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        auth_test = authenticate(username='nobody', password='topsecret')
        self.assertEqual(auth_test, None)

    def test_manual_authentication_fail_inactive(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        user.is_active = False
        user.save()
        auth_test = authenticate(username='jacob', password='topsecret')
        self.assertNotEqual(auth_test, None)
        self.assertFalse(auth_test.is_active)

    def test_login_through_client(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        client = Client()
        client.login(username='jacob', password='topsecret')
        response = client.get('/')

    def test_notloggedin_through_client(self):
        client = Client()
        response = client.get('/')

    def test_login_through_client_and_view_profile(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        client = Client()
        client.login(username='jacob', password='topsecret')
        response = client.get('/profile/view/jacob/')
        self.assertEqual(response.context['user_profile'].user.email,
                         'jacob@gmail.com')

    def test_user_profile_generation(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        profile = UserProfile.objects.get_or_create_profile(user)
        self.assertNotEqual(profile, None)

    def test_user_profile_view(self):
        user = self.user_model.objects.create_user(username='jacob',
                                                   email='jacob@gmail.com',
                                                   password='topsecret')
        profile = UserProfile.objects.get_or_create_profile(user)
        profile.openToEmploy = True
        profile.phone_number = '+999999999'
        profile.github = 'github.com/jacob'
        profile.linkedin = 'linkedin.com/jacob'
        profile.personal = 'jacob.com/im_the_best'
        profile.showPastProjects = True
        profile.showRatings = True
        profile.save()
        client = Client()
        client.login(username='jacob', password='topsecret')
        response = client.get('/profile/view/jacob/')
        response_profile = response.context['user_profile']
        self.assertTrue(response_profile.openToEmploy)
        self.assertEqual(response_profile.phone_number, '+999999999')
        self.assertEqual(response_profile.github, 'github.com/jacob')
        self.assertEqual(response_profile.linkedin, 'linkedin.com/jacob')
        self.assertEqual(response_profile.personal, 'jacob.com/im_the_best')
        self.assertTrue(response_profile.showPastProjects)
        self.assertTrue(response_profile.showRatings)
