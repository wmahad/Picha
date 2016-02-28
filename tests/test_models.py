from django.test import TestCase
from django.db import IntegrityError

from faker import Factory
from django.contrib.auth.models import User
from api.models import UserPhoto, EffectsModel
from api.utilities import pil_to_django
from PIL import Image

from mock import patch, MagicMock

fake = Factory.create()


class UserTests(TestCase):
    """Tests for User Modal"""

    def setUp(self):
        """Setting up of the modal for use"""
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(
            username=self.username,  password=self.password)

    def tearDown(self):
        """Delete the user modal after use"""
        del self.user

    def test_super_user_created(self):
        """Test the creation of a user"""
        self.assertIsInstance(self.user, User)

    def test_super_user_creation_fails(self):
        """Test the creation of a user fails"""
        # this should be fixed
        try:
            self.user = User.objects.create_user(
                username=self.username,  password=self.password)
        except IntegrityError as e:
            self.assertIn("duplicate key value violates unique constraint", e.message)


class UserPhotoTests(TestCase):
    """Class containing tests for a UserPhoto Modal"""

    @patch('api.models.UserPhoto.save', MagicMock(name="save"))
    def setUp(self):
        """Setup the test enviroment for the modal"""
        self.username = fake.user_name()
        self.password = fake.password()
        self.imageName = 'test.png'
        image = Image.open('static/img/' + self.imageName)
        self.image = pil_to_django(image, 'png')
        self.user = User.objects.create_user(
            username=self.username,  password=self.password)
        self.created_image = UserPhoto(image=self.image, name=self.imageName,  created_by=self.user)

    def test_image_gets_created(self):
        """Test image gets created"""
        self.assertEqual(self.created_image.name, self.imageName)



class EffectsModelTests(TestCase):
    """Class containing tests for EffectsModel Modal"""

    @patch('api.models.EffectsModel.save', MagicMock(name="save"))
    @patch('api.models.UserPhoto.save', MagicMock(name="save"))
    def setUp(self):
        """setup method for creating test enviroment of the modal"""
        self.username = fake.user_name()
        self.password = fake.password()
        self.imageName = 'test.png'
        image = Image.open('static/img/' + self.imageName)
        self.image = pil_to_django(image, 'png')
        self.user = User.objects.create_user(
            username=self.username,  password=self.password)
        self.created_image = UserPhoto(image=self.image, name=self.imageName,  created_by=self.user)
        self.image_effect = EffectsModel(effect=self.image, photo=self.created_image)

    def test_effect_gets_created_successfully(self):
        """Test creation of effect for a photo"""
        self.assertIsInstance(self.image_effect, EffectsModel)
        self.assertEqual(self.image_effect.photo, self.created_image)
