import os
import StringIO
import urllib2
from urlparse import urlparse
from django.core.files.base import ContentFile

# define extensions object
extensions = {
	'jpg': 'JPEG',
	'jpeg': 'JPEG',
	'png': 'PNG',
	'gif': 'GIF'
}

def split_url(url):
    """method that splits the url returns server address and path to doc"""
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path

def get_url_tail(url):
    """gets the file name from the url"""
    return url.split('/')[-1]  

def get_extension(filename):
    """gets the extension from the file name"""
    return filename.split('.')[-1]

def pil_to_django(image, ext):
    """returns format of the file into something django understands"""
    fobject = StringIO.StringIO()
    image.save(fobject, format=extensions[ext.lower()])
    return ContentFile(fobject.getvalue())


def retrieve_image(url):
    """returns image from a given image"""
    return StringIO.StringIO(urllib2.urlopen(url).read())