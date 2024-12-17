from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.login_url = reverse('users:token_obtain_pair')  # Login endpoint
        self.refresh_url = reverse('users:token_refresh')   # Token refresh endpoint
        self.logout_url = reverse('users:logout')          # Logout endpoint

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",  # Use email
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",  # Use email
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_logout_failure(self):
        # Obtain a valid access token for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Authenticate with the access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Send an invalid refresh token
        response = self.client.post(self.logout_url, {"refresh": "invalidrefresh"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


    def test_logout_success(self):
        # Obtain a valid refresh token for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Authenticate with the access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Send the refresh token to the logout endpoint
        response = self.client.post(self.logout_url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout successful.")

class SignupTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('users:signup')

    def test_signup_success(self):
        """Test that a user can sign up with valid data."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "User created successfully.")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_password_mismatch(self):
        """Test that signup fails when passwords do not match."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "WrongPassword123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", response.data["error"])

    def test_signup_missing_fields(self):
        """Test that signup fails when required fields are missing."""
        data = {
            "username": "",
            "email": "",
            "password": "",
            "confirm_password": ""
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("All fields are required.", response.data["error"])

    def test_signup_invalid_password(self):
        """Test that signup fails when the password is too weak."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "123",
            "confirm_password": "123"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check partial matches for error messages
        self.assertTrue(any("too short" in err for err in response.data["error"]))
        self.assertTrue(any("too common" in err for err in response.data["error"]))
        self.assertTrue(any("entirely numeric" in err for err in response.data["error"]))

    def test_signup_duplicate_username(self):
        """Test that signup fails when the username is already taken."""
        # Create an existing user
        User.objects.create_user(username="newuser", email="newuser@example.com", password="StrongPassword123!")

        data = {
            "username": "newuser",
            "email": "newuser2@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data["error"])

    def test_duplicate_email_signup_fails(self):
        """Test that signup fails when using an email that already exists."""
        data = {
            "username": "newuser",
            "email": "testuser@example.com",  # Duplicate email
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with this email already exists.", response.data["error"])


class EmailAsPrimaryKeyTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('users:signup')
        # Create an initial user
        User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
        )

    def test_email_as_primary_key(self):
        """Test that email is the primary key."""
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.pk, "testuser@example.com")

    def test_unique_username_with_same_email_fails(self):
        data = {
            "username": "anotheruser",
            "email": "testuser@example.com",  # Duplicate email
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with this email already exists.", response.data["error"])