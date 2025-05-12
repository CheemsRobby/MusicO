from django.db import models
from django.contrib.auth import get_user_model
from apps.music.models import Song

User = get_user_model()

class UserSimilarity(models.Model):
    """用户相似度模型，用于协同过滤"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similar_users')
    similar_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similar_to')
    similarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'similar_user']
        ordering = ['-similarity_score']

class SongSimilarity(models.Model):
    """歌曲相似度模型，用于基于内容的推荐"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='similar_songs')
    similar_song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='similar_to')
    similarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['song', 'similar_song']
        ordering = ['-similarity_score']

class UserRecommendation(models.Model):
    """用户推荐记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=50)  # 'collaborative', 'content', 'popular'
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'song']
        ordering = ['-score', '-created_at']

class SongFeature(models.Model):
    """歌曲特征模型，用于基于内容的推荐"""
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='features')
    tempo = models.FloatField(null=True, blank=True)  # 节奏
    energy = models.FloatField(null=True, blank=True)  # 能量
    danceability = models.FloatField(null=True, blank=True)  # 可舞性
    valence = models.FloatField(null=True, blank=True)  # 情绪
    acousticness = models.FloatField(null=True, blank=True)  # 原声度
    instrumentalness = models.FloatField(null=True, blank=True)  # 器乐度
    liveness = models.FloatField(null=True, blank=True)  # 现场感
    speechiness = models.FloatField(null=True, blank=True)  # 语音度
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class UserPreference(models.Model):
    """用户偏好模型，用于个性化推荐"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    preferred_genres = models.JSONField(default=list)
    preferred_artists = models.JSONField(default=list)
    preferred_decades = models.JSONField(default=list)
    preferred_moods = models.JSONField(default=list)
    preferred_tempo_range = models.JSONField(default=list)
    preferred_energy_range = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

class RecommendationTask(models.Model):
    """推荐任务模型，用于异步处理推荐"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    task_type = models.CharField(max_length=50)  # 'collaborative', 'content', 'hybrid'
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 