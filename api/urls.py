from django.conf.urls import url
# from django.contrib import auth
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    url(r'^register/', views.social_register, name='login'),
    url(r'^photos/', views.PhotoListView.as_view(), name='photos'),
    url(r'^modify_photo/', views.PhotoDetailView.as_view(), name='photodetail'),
    url(r'^filters/', views.apply_filters, name='filters'),
    url(r'^degree/', views.apply_rotations , name='degree'),
    url(r'^text/', views.draw_text , name='text'),
    url(r'^reset/', views.reset_effects , name='reset'),
    url(r'^image/', views.get_uploaded_image , name='image'),
    url(r'^enhancement/', views.apply_enhancement , name='enhancement'),
    url(r'^imageeffects/', views.EffectListView.as_view() , name='imageeffects'),
    url(r'^logout/', 'django.contrib.auth.views.logout' , name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns) 


