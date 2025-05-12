from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserSimilarityViewSet, SongSimilarityViewSet,
    UserRecommendationViewSet, SongFeatureViewSet,
    UserPreferenceViewSet, RecommendationTaskViewSet
)

router = DefaultRouter()
router.register(r'user-similarities', UserSimilarityViewSet, basename='user-similarity')
router.register(r'song-similarities', SongSimilarityViewSet, basename='song-similarity')
router.register(r'recommendations', UserRecommendationViewSet, basename='recommendation')
router.register(r'song-features', SongFeatureViewSet, basename='song-feature')
router.register(r'preferences', UserPreferenceViewSet, basename='preference')
router.register(r'tasks', RecommendationTaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
] 