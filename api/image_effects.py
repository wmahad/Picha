from PIL import Image, ImageFilter


temp_url = 'static/media/temp/'

"""this module will handle the effect transformations on an image with pillow"""

def blur_filter(imageUrl, image_name):
	"""Method blurs the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.GaussianBlur(radius=2))
	image.save(temp_url + "BLUR" + image_name)
	return temp_url + "BLUR" + image_name

def contour_filter(imageUrl, image_name):
	"""Method applys the contour effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.CONTOUR)
	image.save(temp_url + "CONTOUR" + image_name)
	return temp_url + "CONTOUR" + image_name

def detail_filter(imageUrl, image_name):
	"""Method applys the detail effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.DETAIL)
	image.save(temp_url + "DETAIL" + image_name)
	return temp_url + "DETAIL" + image_name

def edge_enhance_filter(imageUrl, image_name):
	"""Method applys the edge enhance effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.EDGE_ENHANCE)
	image.save(temp_url + "EDGE_E" + image_name)
	return temp_url + "EDGE_E" + image_name

def embos_filter(imageUrl, image_name):
	"""Method applys the embos effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.EMBOSS)
	image.save(temp_url + "EMBOS" + image_name)
	return temp_url + "EMBOS" + image_name

def find_edges_filter(imageUrl, image_name):
	"""Method applys the find edge effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.FIND_EDGES)
	image.save(temp_url + "FIND_EDGE" + image_name)
	return temp_url + "FIND_EDGE" + image_name

def smooth_filter(imageUrl, image_name):
	"""Method applys the smooth effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.SMOOTH)
	image.save(temp_url + "SMOOTH" + image_name)
	return temp_url + "SMOOTH" + image_name

def black_n_white_filter(imageUrl, image_name):
	"""Method applys the black and white effect on the image"""
	image = Image.open(imageUrl)
	image = image.convert("L")
	image.save(temp_url + "BLACK_N_WHITE" + image_name)
	return temp_url + "BLACK_N_WHITE" + image_name

def sharpen_filter(imageUrl, image_name):
	"""Method applys the sharpen effect on the image"""
	image = Image.open(imageUrl)
	image = image.filter(ImageFilter.SHARPEN)
	image.save(temp_url + "SHARPEN" + image_name)
	return temp_url + "SHARPEN" + image_name