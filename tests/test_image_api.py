import os

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.test import APITestCase 

from mock import patch, MagicMock
from django.core.files import File

from django.contrib.auth.models import User
from api.models import UserPhoto, EffectsModel
from api.utilities import pil_to_django
from api import views

from faker import Factory
from PIL import Image

fake = Factory.create()



class UserPhotoTests(APITestCase):
	"""
	Tests to do with user registration and login
	"""
	def setUp(self):
		"""Set up user photo specific data"""
		self.username = fake.user_name()
		self.password = fake.password()

		self.image_name = 'test.png'
		self.img_url = 'static/img/test.png'	

		self.user = User.objects.create_user(
			username=self.username,  password=self.password)
		self.user = authenticate(username=self.username, password=self.password)
		self.client.login(username=self.username, password=self.password)

		self.image = Image.frombytes('L', (100, 100), "\x00" * 100 * 100)
		self.image = pil_to_django(self.image, 'png')

		self.created_image = UserPhoto(image=self.image, name=self.image_name,  created_by=self.user).save()
		

	def tearDown(self):
	    """Delete the user modal after use"""
	    del self.user
	    del self.created_image

	@patch('api.models.UserPhoto.save', MagicMock(name="save"))
	def test_user_photo_creation_succeeds(self):
		"""
		tests whether a user gets created when new user signs up
		"""
		image_name = 'test1.png'
		with open(self.img_url, 'rb') as image:			
			data = {'image': image, 'name':image_name}			
			response = self.client.post(reverse('photos'), data)
			image.close()
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data.get('name'), image_name)

	
	def test_retrieval_of_user_photos(self):
		"""
		tests whether user can get back his uploaded images
		"""	
		get_response = self.client.get(reverse('photos'))

		self.assertEqual(get_response.status_code, status.HTTP_200_OK)
		data = [i.values() for i in get_response.data]
		self.assertIn(u'{}'.format(self.image_name), data[0])



class PhotoDetailTests(APITestCase):
	"""
	Tests for a single photo
	"""
	def setUp(self):
		"""Create photo specific variables for testing a single photo"""
		self.username = fake.user_name()
		self.password = fake.password()
		self.image_name = 'test.png'
		self.img_url = 'static/img/test.png'
		self.user = User.objects.create_user(
		    username=self.username,  password=self.password)
		self.image = File(open(self.img_url, 'rb'))

	def tearDown(self):
		"""Delete the user modal after use"""
		del self.user
		del self.image


	def test_user_photo_retrieval_by_id_succeeds(self):
		"""
		tests whether a user gets created when new user signs up
		"""
		# url = reverse('photodetail')	
		self.created_image = UserPhoto(image=self.image, name=self.image_name,  created_by=self.user)
		self.created_image.save()
		response = self.client.get('/api/modify_photo/?id={}'.format(self.created_image.id))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('name'), self.image_name)
		os.remove('static/media/' + str(self.created_image.image))
		del self.created_image

	def test_user_photo_retrieval_by_name_succeeds(self):
		"""
		tests whether a user gets created when new user signs up
		"""
		# url = reverse('photodetail')	
		self.created_image = UserPhoto(image=self.image, name=self.image_name,  created_by=self.user)
		self.created_image.save()
		response = self.client.get('/api/image/?name={}'.format(self.created_image.name))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('name'), self.image_name)
		os.remove('static/media/' + str(self.created_image.image))
		del self.created_image		

	def test_deletion_of_user_photo_succeeds(self):
		"""
		tests whether user can get back his uploaded images
		"""
		self.name = 'media.png'
		self.image = File(open('static/img/media.png', 'rb'))
		self.created_image = UserPhoto(image=self.image, name=self.name,  created_by=self.user)
		self.created_image.save()			
		response = self.client.delete('/api/modify_photo/?id={}'.format(self.created_image.id))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)