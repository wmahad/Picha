from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase 

from mock import patch, MagicMock

from api import views


class MockResponse(object):

    def __init__(self, resp_data, code=200):
        self.resp_data = resp_data
        self.code = code
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        """return """
        return self.resp_data

    def getcode(self):
        return self.code

class ImageEffects(APITestCase):
    
	def setUp(self):
	    "Mock urllib2.urlopen"
	    self.patcher = patch('urllib2.urlopen')
	    self.urlopen_mock = self.patcher.start()
	    
	def test_application_of_image_filters(self):
		"""
		tests that filters get applied to an image
		"""
		ret = {
		    'image_url': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg'
		}

		self.urlopen_mock.return_value =  MockResponse(ret)

		data = {'image_url': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg'}
		response = self.client.get(reverse("filters"), data)
		self.assertEqual(response.status_code, 200)
		response = self.client.get(reverse('reset'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_application_of_image_enhancements(self):
		"""
		tests that enhancements get applied to an image
		"""
		ret = {
		    'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg'
		}

		self.urlopen_mock.return_value =  MockResponse(ret)

		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'x':4, 'y': 2, 'w':2, 'z':1
			}
		response = self.client.get(reverse("enhancement"), data)
		self.assertEqual(response.status_code, 200)
		response = self.client.get(reverse('reset'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_image_rotation(self):
		"""
		tests that image gets rotated 
		"""
		ret = {
		    'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg'
		}

		self.urlopen_mock.return_value =  MockResponse(ret)
		# flip verticle
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'x':0}
		response = self.client.get(reverse("degree"), data)
		self.assertEqual(response.status_code, 200)
		# rotate left
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'x':1}
		response = self.client.get(reverse("degree"), data)
		self.assertEqual(response.status_code, 200)
		# rotate right
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'x':2}
		response = self.client.get(reverse("degree"), data)
		self.assertEqual(response.status_code, 200)
		# flip horizontal
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'x':4}
		response = self.client.get(reverse("degree"), data)
		self.assertEqual(response.status_code, 200)
		# reset everything
		response = self.client.get(reverse('reset'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_text_gets_drawn_on_image(self):
		"""
		tests that text from a user gets drawn on the image 
		"""
		ret = {
		    'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg'
		}

		self.urlopen_mock.return_value =  MockResponse(ret)
		# draw text on the top left
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'topleft'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the mid left
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'left'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the bottom left
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'bottomleft'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the top right
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'topright'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the top right
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'right'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the  right
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'bottomright'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the center
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'center'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the top 
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'top'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# draw text on the bottom
		data = {'image': 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/f9af0618846673.562d053f70803.jpg',
				'text':'dummy text', 'position': 'bottom'}
		response = self.client.get(reverse("text"), data)
		self.assertEqual(response.status_code, 200)
		# reset everything
		response = self.client.get(reverse('reset'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def tearDown(self):
	    self.patcher.stop()