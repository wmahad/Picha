from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import UserPhoto, EffectsModel

class PhotoSerializer(serializers.ModelSerializer):
	"""Serializer class for UserPhoto's model"""
	class Meta:
		"""Meta class that defines meta data info about the serializer class"""
		model = UserPhoto
		fields = ( 'id', 'image', 'name', 'date_created', 'date_modified', )
		read_only_fields = ('date_created', 'date_modified',)


class ImageSerializer(serializers.ModelSerializer):
	"""Serializer class for UserPhoto's model"""
	# the next line appends server and port address in front of the image
	# it returns absolute url of image from the server
	image_url = serializers.SerializerMethodField('generate_image_url')
	class Meta:
		"""Meta class that defines meta data info about the serializer class"""
		model = UserPhoto
		fields = ( 'id', 'image', 'name', 'image_url', )

	def generate_image_url(self, obj):
		"""retun absolute path to the image from the server"""
		return self.context['request'].build_absolute_uri(obj.image.url)
		

class EffectSerializer(serializers.ModelSerializer):
	"""docstring for EffectsSerializers"""
	class Meta:
		"""Meta class that defines meta data info about the serializer class"""
		model = EffectsModel
		fields = ('id', 'effect', 'photo', )
			
		