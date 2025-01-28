from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
import tempfile
import shutil
import os

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class TestCreateUserView(TestCase):
    def setUp(self):
        self.client         = APIClient()
        self.valid_data     = {"username": "testuser", "password": "securepassword123"}
        self.invalid_data   = {"username": "", "password": "short"}
        self.duplicate_data = {"username": "testuser", "password": "securepassword456"}
        self.url            = reverse("register")

    def test_create_user_success(self):
        response = self.client.post(self.url, self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_create_user_failure_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_user_failure_duplicate_username(self):        
        self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.duplicate_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"][0], "A user with that username already exists.")

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestUpdateUserView(TestCase):
    def setUp(self):
        self.client                 = APIClient()
        self.user                   = User.objects.create_user(username="testuser", password="securepassword123")
        self.client.force_authenticate(user=self.user)
        self.valid_update_data      = {"username": "updateduser"}
        self.invalid_update_data    = {"username": ""}
        self.no_change_data         = {"username": self.user.username}
        self.invalid_password_data  = {"password": "short"}
        self.empty_request_data     = {}
        self.test_image_path        = os.path.join("media", "profile_pictures", "test_image.jpg")
        with open(self.test_image_path, "rb") as img_file:
            self.test_image         = SimpleUploadedFile("test_image.jpg", img_file.read(), content_type="image/jpeg")
        self.multi_update_data      = {"username": "newusername", "profile_picture": self.test_image}
        self.url                    = reverse("update-user")
    
    def tearDown(self):
        shutil.rmtree(tempfile.gettempdir(), ignore_errors=True)
        
    def test_update_user_success_username_change(self):
        response = self.client.patch(self.url, self.valid_update_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        
    def test_update_user_success_password_change(self):
        valid_password_data = {"password": "newsecurepassword123"}
        response            = self.client.patch(self.url, valid_password_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword123"))
        
    def test_partial_update_user_success_with_image(self):
        response = self.client.patch(self.url, {"profile_picture": self.test_image}, format="multipart")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile_picture.name.startswith("profile_pictures/"))
        self.assertIn("test_image", self.user.profile_picture.name)
        
    def test_update_user_success_multiple_fields(self):
        response = self.client.patch(self.url, self.multi_update_data, format="multipart") 
               
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, self.multi_update_data["username"])
        self.assertTrue(self.user.profile_picture.name.startswith("profile_pictures/"))
        self.assertIn("test_image", self.user.profile_picture.name)

    def test_update_user_unauthorized(self):
        self.client.logout()
        response = self.client.patch(self.url, self.valid_update_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_failure_invalid_data(self):
        response = self.client.patch(self.url, self.invalid_update_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_update_user_failure_no_changes(self):
        response = self.client.patch(self.url, self.no_change_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No changes detected.")

    def test_update_user_failure_invalid_password(self):
        response = self.client.patch(self.url, self.invalid_password_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_update_user_failure_empty_request(self):
        response = self.client.patch(self.url, self.empty_request_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No data provided to update.")

class TestDeleteUserView(TestCase):
    def setUp(self):
        self.client         = APIClient()
        self.user           = User.objects.create_user(username="testuser", password="securepassword123")
        self.client.force_authenticate(user=self.user)
        self.valid_data     = {"password": "securepassword123"}
        self.invalid_data   = {"password": "wrongpassword"}
        self.url            = reverse("delete-user")

    def test_delete_user_success(self):
        response = self.client.delete(self.url, data=self.valid_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_delete_user_failure_invalid_password(self):
        response = self.client.delete(self.url, data=self.invalid_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
     
    def test_delete_user_failure_missing_password(self):
        response = self.client.delete(self.url, data={}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(username="testuser").exists())   

class TestUserProfileView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="securepassword123")
        self.client.force_authenticate(user=self.user)
        self.url         = reverse("user-profile")

    def test_fetch_user_profile(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestUploadProfilePictureView(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.user       = User.objects.create_user(username="testuser", password="securepassword123")
        self.client.force_authenticate(user=self.user)
        self.fake_image = SimpleUploadedFile(name="test_image.jpg", content=b"fake image content", content_type="image/jpeg")
        self.url        = reverse("upload-profile-picture")
        
    def tearDown(self):
        shutil.rmtree(tempfile.gettempdir(), ignore_errors=True)

    def test_upload_profile_picture_success(self):
        response = self.client.post(self.url, {"profile_picture": self.fake_image}, format="multipart")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_profile_picture_failure_no_file(self):
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLogoutView(TestCase):
    def setUp(self):
        self.client         = APIClient()
        self.user           = User.objects.create_user(username="testuser", password="securepassword123")
        self.client.force_authenticate(user=self.user)
        token_url           = reverse("token-obtain-pair")
        response            = self.client.post(token_url, {"username": "testuser", "password": "securepassword123"})
        self.refresh_token  = response.data["refresh"]
        self.url            = reverse("logout")

    def test_logout_success(self):
        response = self.client.post(self.url, {"refresh": self.refresh_token}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    def test_logout_failure_missing_token(self):
        response = self.client.post(self.url, {}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
