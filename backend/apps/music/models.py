from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Artist(models.Model):
    """音乐艺术家模型"""
    name = models.CharField(_('name'), max_length=100)
    bio = models.TextField(_('biography'), blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='artists/', null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('artist')
        verbose_name_plural = _('artists')
        ordering = ['name']

    def __str__(self):
        return self.name

class Album(models.Model):
    """专辑模型"""
    title = models.CharField(_('title'), max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(_('cover'), upload_to='albums/', null=True, blank=True)
    release_date = models.DateField(_('release date'), null=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    genre = models.CharField(_('genre'), max_length=50, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')
        ordering = ['-release_date', 'title']

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

class Song(models.Model):
    """歌曲模型"""
    title = models.CharField(_('title'), max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', null=True, blank=True)
    audio_file = models.FileField(_('audio file'), upload_to='songs/')
    duration = models.DurationField(_('duration'))
    lyrics = models.TextField(_('lyrics'), blank=True)
    genre = models.CharField(_('genre'), max_length=50, blank=True)
    language = models.CharField(_('language'), max_length=50, blank=True)
    release_date = models.DateField(_('release date'), null=True, blank=True)
    play_count = models.PositiveIntegerField(_('play count'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    def increment_play_count(self):
        """增加播放次数"""
        self.play_count += 1
        self.save()

class Playlist(models.Model):
    """播放列表模型"""
    title = models.CharField(_('title'), max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    description = models.TextField(_('description'), blank=True)
    cover = models.ImageField(_('cover'), upload_to='playlists/', null=True, blank=True)
    is_public = models.BooleanField(_('is public'), default=True)
    songs = models.ManyToManyField(Song, through='PlaylistSong', related_name='playlists')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlists')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class PlaylistSong(models.Model):
    """播放列表歌曲关联模型"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_('order'))
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)

    class Meta:
        verbose_name = _('playlist song')
        verbose_name_plural = _('playlist songs')
        ordering = ['order']
        unique_together = ['playlist', 'song']

    def __str__(self):
        return f"{self.playlist.title} - {self.song.title}"

class UserListeningHistory(models.Model):
    """用户收听历史模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(_('listened at'), auto_now_add=True)
    duration = models.DurationField(_('duration'))
    device = models.CharField(_('device'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('listening history')
        verbose_name_plural = _('listening histories')
        ordering = ['-listened_at']

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"

class SongRating(models.Model):
    """歌曲评分模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(_('rating'))
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('song rating')
        verbose_name_plural = _('song ratings')
        unique_together = ['user', 'song']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.song.title} - {self.rating}" 