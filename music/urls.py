from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
from django.urls import path
from .views import index, upload_music, player

urlpatterns = [
    path('', index, name='index'),
    path('upload_music/', upload_music, name='upload_music'),
]
from django.urls import path
from .views import index, upload_music, user_login, user_register, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('upload_music/', upload_music, name='upload_music'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('player/', player, name='player'),
]