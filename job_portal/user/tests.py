from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.auth.hashers import make_password

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user_password = 'test_password'
        self.user_email = 'test@example.com'
        self.user_role = 'C'
        self.user = User.objects.create(
            email=self.user_email,
            password=self.user_password,
            role=self.user_role,
        )

    def test_login_view(self):
        response = self.client.get(reverse('clogin'))
        self.assertEqual(response.status_code, 200)

        # Test login with valid credentials
        response = self.client.post(reverse('clogin'), {
            'email': self.user_email,
            'password': self.user_password,
        })
        self.assertRedirects(response, '/candidates/createProfile') # Change the redirect URL based on the user role

        self.client.get(reverse('logout')) # logging out before logging in again

        # Test login with invalid credentials
        response = self.client.post(reverse('clogin'), {
            'email': self.user_email,
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 200)

    def test_registration_view(self):
        response = self.client.get(reverse('cregister'))
        self.assertEqual(response.status_code, 200)

        # Test registration with valid data
        response = self.client.post(reverse('cregister'), {
            'email': 'new_user@example.com',
            'password': 'new_password',
            'role': 'C',
        })
        self.assertRedirects(response, '/candidates/createProfile') # Change the redirect URL based on the user role
        self.client.get(reverse('logout')) # logging out before registering again

        # Test registration with existing email
        response = self.client.post(reverse('cregister'), {
            'email': self.user_email,
            'password': 'new_password',
            'role': 'C',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_logout_view(self):
        # Login first to set the session
        response = self.client.post(reverse('clogin'), {
            'email': self.user_email,
            'password': self.user_password,
        })
       
        response = self.client.get(reverse('clogout'))
        self.assertRedirects(response, '/')
        self.assertNotIn("is_authenticated", self.client.session)
