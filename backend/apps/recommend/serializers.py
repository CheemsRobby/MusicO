from rest_framework import serializers
from .models import (
    UserSimilarity, SongSimilarity, UserRecommendation,
    SongFeature, UserPreference, RecommendationTask
)
from apps.music.serializers import SongSerializer
from apps.user.serializers import UserSerializer

class UserSimilaritySerializer(serializers.ModelSerializer):
    similar_user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSimilarity
        fields = ('id', 'user', 'similar_user', 'similarity_score', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')

class SongSimilaritySerializer(serializers.ModelSerializer):
    similar_song = SongSerializer(read_only=True)
    
    class Meta:
        model = SongSimilarity
        fields = ('id', 'song', 'similar_song', 'similarity_score', 'created_at', 'updated_at')
        read_only_fields = ('song', 'created_at', 'updated_at')

class UserRecommendationSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = UserRecommendation
        fields = ('id', 'user', 'song', 'recommendation_type', 'score', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')

class SongFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongFeature
        fields = (
            'id', 'song', 'tempo', 'energy', 'danceability',
            'valence', 'acousticness', 'instrumentalness',
            'liveness', 'speechiness', 'created_at', 'updated_at'
        )
        read_only_fields = ('song', 'created_at', 'updated_at')

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = (
            'id', 'user', 'preferred_genres', 'preferred_artists',
            'preferred_decades', 'preferred_moods',
            'preferred_tempo_range', 'preferred_energy_range',
            'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')

class RecommendationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationTask
        fields = (
            'id', 'user', 'status', 'task_type',
            'result', 'error_message', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')

class RecommendationRequestSerializer(serializers.Serializer):
    recommendation_type = serializers.ChoiceField(
        choices=['collaborative', 'content', 'hybrid', 'popular'],
        default='hybrid'
    )
    limit = serializers.IntegerField(min_value=1, max_value=100, default=10)
    include_explanation = serializers.BooleanField(default=False)
    use_preferences = serializers.BooleanField(default=True)
    refresh = serializers.BooleanField(default=False) 