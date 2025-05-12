from django.urls import path, include
from rest_framework.routers import DefaultRouter
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