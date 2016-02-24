import os, datetime
from django.db import models
from django.contrib.auth.models import User

def generate_upload_path(self, filename):
	"""Method to generate new image name and path to where it will be stored
				it takes in a file name and returns path"""
	filename, ext = os.path.splitext(filename.lower())
	filename = "IMG_{0}{1}".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"), ext)
	return 'effects/{0}'.format(filename)

class UserPhoto(models.Model):
	"""docstring for UserPhotos Model
	Stores image path and name
	"""
	image = models.FileField(upload_to="%Y/%m/%d")
	name = models.CharField(blank=False, unique=True, max_length=100)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)	


class EffectsModel(models.Model):
	"""docstring for UserPhotos
	Stores original Image ID and path to the effects applied to the image
	"""
	effect = models.FileField(upload_to=generate_upload_path)
	date_created = models.DateTimeField(auto_now_add=True)
	photo = models.ForeignKey(UserPhoto)	
		

		