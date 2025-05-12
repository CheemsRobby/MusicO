from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for the music recommendation system."""
    
    # Basic profile fields
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Music preferences
    favorite_genres = models.JSONField(default=list, blank=True)
    favorite_artists = models.JSONField(default=list, blank=True)
    
    # Social fields
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    
    # Privacy settings
    is_private = models.BooleanField(default=False)
    
    # Activity tracking
    last_active = models.DateTimeField(auto_now=True)
    total_listening_time = models.DurationField(default=0)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def update_listening_time(self, duration):
        """Update user's total listening time."""
        self.total_listening_time += duration
        self.save()
    
    def update_followers_count(self):
        """Update followers count."""
        self.followers_count = self.followers.count()
        self.save()
    
    def update_following_count(self):
        """Update following count."""
        self.following_count = self.following.count()
        self.save()

class UserProfile(models.Model):
    """Extended user profile with detailed music preferences."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Music preferences
    preferred_languages = models.JSONField(default=list, blank=True)
    preferred_decades = models.JSONField(default=list, blank=True)
    preferred_moods = models.JSONField(default=list, blank=True)
    
    # Listening habits
    preferred_listening_times = models.JSONField(default=list, blank=True)
    preferred_listening_devices = models.JSONField(default=list, blank=True)
    
    # Discovery preferences
    discovery_preferences = models.JSONField(default=dict, blank=True)
    
    # Activity tracking
    last_recommendation_update = models.DateTimeField(null=True, blank=True)
    recommendation_history = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def update_recommendation_history(self, recommendation):
        """Update recommendation history."""
        self.recommendation_history.append(recommendation)
        self.save()
    
    def get_preferences(self):
        """Get user's music preferences."""
        return {
            'genres': self.user.favorite_genres,
            'languages': self.preferred_languages,
            'decades': self.preferred_decades,
            'moods': self.preferred_moods,
        } 