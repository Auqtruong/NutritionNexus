from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepassword123")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("securepassword123"))
        self.assertEqual(self.user.profile_picture.name, "profile_pictures/default.jpg")

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser")

    def test_profile_picture_upload(self):
        test_image = SimpleUploadedFile(
            name="test_image.jpg", 
            content=b"fake image content", 
            content_type="image/jpeg"
        )
        self.user.profile_picture = test_image
        self.user.save()
        
        self.assertTrue(self.user.profile_picture.name.startswith("profile_pictures/"))
        self.assertIn("test_image", self.user.profile_picture.name)

    def test_username_uniqueness_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="testuser", password="anotherpassword")

    def test_profile_picture_defaults_if_not_set(self):
        new_user = User.objects.create_user(username="newuser", password="password123")
        
        self.assertEqual(new_user.profile_picture.name, "profile_pictures/default.jpg")
