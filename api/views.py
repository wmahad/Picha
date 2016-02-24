import urllib
import cStringIO
import os

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from social.apps.django_app.utils import load_strategy, load_backend
from social.exceptions import AuthAlreadyAssociated

from api.serializers import PhotoSerializer, ImageSerializer, EffectSerializer
from api.models import UserPhoto, EffectsModel
from api.permissions import IsAuthenticatedOrCreate
from api import utilities
from api import image_effects

from PIL import Image, ImageEnhance, ImageDraw, ImageFont     
        
@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def social_register(request):
    """Viewset for handling facebook authentication"""
    if request.method == 'POST':
        auth_token = request.data['access_token']
        backend = request.data['backend']
        if auth_token and backend:
            strategy = load_strategy(request)
            backend = load_backend(
                strategy=strategy, name=backend, redirect_uri=None)
            # do backend authentication and check if account is already associated
            try:
                user = backend.do_auth(auth_token)
            except AuthAlreadyAssociated:
                return Response({"errors": "That social media account is already in use"},
                                status=status.HTTP_400_BAD_REQUEST)
            # if a user has been created log the user in
            if user:
                login(request, user)
                return Response( {'user' : user.username}, status=status.HTTP_200_OK )
            else:
                return Response("Bad Credentials", status=403)
        else:
            return Response("Bad request", status=400)


class PhotoListView(generics.ListCreateAPIView):
    """The view set for photo creation and upload"""
    # Setting permission classes
    permission_classes = (IsAuthenticatedOrCreate, permissions.IsAuthenticated)

    queryset = UserPhoto.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        """Method for handling the actual creation and upload"""
        serializer = PhotoSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        """Modify query to display photos for logged in user"""
        user = self.request.user
        return UserPhoto.objects.all().filter(created_by=user)


class PhotoDetailView(APIView):
    """The view set for handling photo display"""

    def get(self, request):
        """return photo data specific to a particular id"""
        image = UserPhoto.objects.get(id=request.query_params['id'])
        serializer = PhotoSerializer(image, context={'request': request})
        # return serialized data
        return Response(serializer.data)

    def delete(self, request):
        """delete the image record from the database and remove it from the folder too"""
        media_route = 'static/media/'
        image = UserPhoto.objects.get(id=request.query_params['id'])
        image.delete()
        try:
            media_route += str(image.image)
            os.remove(media_route)
        except Exception, e:
            print("Error: file not found: {0}".format(e))                
        # delete it only if it has been removed from the folder
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_uploaded_image(request):
    """retrieve an uploaded image basing on its name"""
    if request.method == 'GET':
        image_object = UserPhoto.objects.get(name=request.query_params['name'])
        serializer = ImageSerializer(image_object, context={'request': request})
        return Response(serializer.data)
        
@api_view(['GET'])
def reset_effects(request):
    """the view handles resetion of effects generated"""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'
        # read all files in a folder and delete them
        file_list = os.listdir(temp_url)
        for file_name in file_list:
            os.remove(temp_url+"/"+file_name)
        
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def apply_filters(request):
    """view handles setting of filters on the image"""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'        
        
        image_url = request.query_params['image_url']
        file_name = image_url.rsplit('/', 1)[-1]
        
        file_ = cStringIO.StringIO(urllib.urlopen(image_url).read() )      
        
        
        data = {
            'BLUR': image_effects.blur_filter(file_, file_name),
            'CONTOUR': image_effects.contour_filter(file_, file_name),
            'DETAIL': image_effects.detail_filter(file_, file_name),
            'EDGE_ENHANCE': image_effects.edge_enhance_filter(file_, file_name),
            'EMBOS': image_effects.embos_filter(file_, file_name),
            'FIND_EDGES': image_effects.find_edges_filter(file_, file_name),
            'SMOOTH': image_effects.smooth_filter(file_, file_name),
            'BAW': image_effects.black_n_white_filter(file_, file_name),
            'SHARPEN': image_effects.sharpen_filter(file_, file_name)
        }

        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def apply_enhancement(request):
    """view handles enhancement effects on an image"""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'

        image_url = request.query_params['image']
        color = int(request.query_params['x'])
        contrast = int(request.query_params['y'])
        sharpness = int(request.query_params['w'])
        brightness = int(request.query_params['z'])

        file_name = image_url.rsplit('/', 1)[-1]
        file_ = cStringIO.StringIO(urllib.urlopen(image_url).read())

        new_image_url = temp_url + "Enhance" + file_name

        image = Image.open(file_)

        if color != 0:
            # when color is not zero enhancement the image
            enhancer = ImageEnhance.Color(image.convert('RGB'))
            image = enhancer.enhance(color / 2.0)

        
        if contrast != 0:
            # when contrast is not zero enhancement the image
            enhancer = ImageEnhance.Contrast(image.convert('RGB'))
            image = enhancer.enhance(contrast / 2.0)
        
        if brightness != 0:
            # when brightness is not zero enhancement the image
            enhancer = ImageEnhance.Brightness(image.convert('RGB'))
            image = enhancer.enhance(brightness / 2.0)
        
        if sharpness != 0:
            # when sharpness is not zero enhancement the image
            enhancer = ImageEnhance.Sharpness(image.convert('RGB'))
            image = enhancer.enhance(sharpness / 2.0)
            
        image.save(new_image_url)
        
        return Response({"enhance": new_image_url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def apply_rotations(request):
    """view handles rotation of the image"""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'

        image_url = request.query_params['image']
        degree = int(request.query_params['x'])

        file_name = image_url.rsplit('/', 1)[-1]

        file_ = cStringIO.StringIO(urllib.urlopen(image_url).read())

        new_image_url = temp_url + "Degree" + file_name

        image = Image.open(file_)
        if degree == 0:
            # flip verticle
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        elif degree == 1:
            # rotate right
            image = image.rotate(-90)
        elif degree == 2:
            # rotate right
            image = image.rotate(90)
        else:
            # flip horizontal
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        image.save(new_image_url)
        
        return Response({"degree": new_image_url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def draw_text(request):
    """view handles drawing of text on an image at a certain location on the image"""
    if request.method == 'GET':
        temp_url = 'static/media/temp/'

        image_url = request.query_params['image']
        text = request.query_params['text']
        position = request.query_params['position']

        file_name = image_url.rsplit('/', 1)[-1]
        file_ = cStringIO.StringIO(urllib.urlopen(image_url).read())

        new_image_url = temp_url + "text" + file_name

        # get an image
        base = Image.open(file_).convert('RGBA')
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', base.size, (255,255,255,0))
        width, height = base.size[0], base.size[1]
        # get a font
        fnt = ImageFont.truetype('static/nimbus.otf', 40)
        # get a drawing context
        drawing_context = ImageDraw.Draw(txt)
        # draw text, half opacity
        # drawing_context.text((10,10), "Hello", font=fnt, fill=(255,255,255,128))
        # draw text, full opacity
        if position == "topleft":
            drawing_context.text((20,90), text, font=fnt, fill=(255,255,255,255))
        elif position == "left":
            drawing_context.text((20,height/2), text, font=fnt, fill=(255,255,255,255))
        elif position == "bottomleft":
            drawing_context.text((20,(height - 100)), text, font=fnt, fill=(255,255,255,255))
        elif position == "center":
            drawing_context.text(((width / 2) - (len(text) * len(text)), height / 2), text, font=fnt, fill=(255,255,255,255))
        elif position == "top":
            drawing_context.text(((width / 2) - (len(text) * len(text)), 90), text, font=fnt, fill=(255,255,255,255))
        elif position == "bottom":
            drawing_context.text(((width / 2) - (len(text) * len(text)), height - 100), text, font=fnt, fill=(255,255,255,255))
        elif position == "topright":
            drawing_context.text((width - (len(text) * len(text)) - 200, 90), text, font=fnt, fill=(255,255,255,255))
        elif position == "right":
            drawing_context.text((width - (len(text) * len(text)) - 200, height / 2), text, font=fnt, fill=(255,255,255,255))
        elif position == "bottomright":
            drawing_context.text((width - (len(text) * len(text)) - 200, height - 100), text, font=fnt, fill=(255,255,255,255))

        output_image = Image.alpha_composite(base, txt)
        output_image.save(new_image_url)

        
        return Response({"image_text": new_image_url}, status=status.HTTP_200_OK)

#class EffectListView(APIView):
#     """The view set for photoeffect creation and upload"""
#     # Setting permission classes
#     permission_classes = (IsAuthenticatedOrCreate, permissions.IsAuthenticated)

#     def post(self, request):
#         """Method for handling the actual creation and upload"""
#         url = request.data['effect']
#         photo_id = request.data['photo_id']
#         # get the domain and the path to the image
#         domain, path = utilities.split_url(url)
#         # get file name of the image
#         filename = utilities.get_url_tail(path)
#         # get cString object
#         fobject = utilities.retrieve_image(url)
#         # Open the image using pill
#         pil_image = Image.open(fobject)
#         # get file name extension
#         ext = utilities.get_extension(filename)
#         # convert image to what django understands
#         image = utilities.pil_to_django(pil_image, ext)
#         user_photo = UserPhoto.objects.get(id=photo_id)
#         image_model = EffectsModel()
#         image_model.photo_id = user_photo.id
#         image_model.effect.save(filename, image)
#         # Save the image and return a response of 201
#         image_model.save()
#         return Response(status=status.HTTP_201_CREATED)


#     def get(self, request):
#         """Modify query to display photos with efects for a particular id"""
#         _id = request.query_params['id']
#         effectsobject = EffectsModel.objects.all()
#         if _id is not None:
#             effectsobject = effectsobject.filter(photo=_id)
#         # serialize returned data
#         serializer = EffectSerializer(effectsobject, context={'request': request}, many=True)
#         return Response(serializer.data)
