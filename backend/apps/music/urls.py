from django.urls import path, include
from rest_framework.routers import DefaultRouter

from music import admin
from music.views import upload_music
from .views import (
    ArtistViewSet, AlbumViewSet, SongViewSet,
    PlaylistViewSet, UserListeningHistoryViewSet,
    SongRatingViewSet
)

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'history', UserListeningHistoryViewSet, basename='history')
router.register(r'ratings', SongRatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from .views import index, player  # 假设你有一个 player 视图

urlpatterns = [
    path('index/', index, name='index'),
    path('upload_music/', upload_music, name='upload_music'),
    path('player/', player, name='player'),  # 添加这一行
]


