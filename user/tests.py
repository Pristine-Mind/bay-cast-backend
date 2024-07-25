from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from user.models import Profile


class RegistrationTest(APITestCase):

    def test_user_registration(self):
        old_user_count = User.objects.filter(is_active=False).count()
        newusr = "testuser@gmail.com"
        data = {
            "email": newusr,
            "username": "tetsts",
            "password": "haA1ScKwEuEs3aX",
            "first_name": "Peter",
            "last_name": "Falk",
            "user_type": Profile.UserType.ADMIN
        }
        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(User.objects.filter(is_active=False).count(), old_user_count)  # No new user to be created

        # update the email now should create user
        data["email"] = "test@gmail.com"
        resp = self.client.post("/register", data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.filter(is_active=True).count(), old_user_count + 1)

        # check profile is created for the user
        self.assertEqual(Profile.objects.filter(user__email=data["email"]).exists(), True)
