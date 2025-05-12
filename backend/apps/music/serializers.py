from rest_framework import serializers
from .models import (
    Artist, Album, Song, Playlist,
    PlaylistSong, UserListeningHistory, SongRating
)

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id', 'name', 'bio', 'avatar',
            'created_at', 'updated_at'
        )

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    
    class Meta:
        model = Album
        fields = (
            'id', 'title', 'artist', 'cover',
            'release_date', 'description', 'genre',
            'created_at', 'updated_at'
        )

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = (
            'id', 'title', 'artist', 'album',
            'audio_file', 'duration', 'lyrics',
            'genre', 'language', 'release_date',
            'play_count', 'is_favorite', 'average_rating',
            'created_at', 'updated_at'
        )
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

class PlaylistSongSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = PlaylistSong
        fields = ('id', 'song', 'order', 'added_at')

class PlaylistSerializer(serializers.ModelSerializer):
    songs = PlaylistSongSerializer(source='playlistsong_set', many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = (
            'id', 'title', 'user', 'description',
            'cover', 'is_public', 'songs', 'song_count',
            'created_at', 'updated_at'
        )
        read_only_fields = ('user',)
    
    def get_song_count(self, obj):
        return obj.songs.count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserListeningHistorySerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = UserListeningHistory
        fields = (
            'id', 'user', 'song', 'listened_at',
            'duration', 'device'
        )
        read_only_fields = ('user',)

class SongRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SongRating
        fields = (
            'id', 'user', 'song', 'rating',
            'comment', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

class SongUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False)
    audio_file = serializers.FileField()
    duration = serializers.DurationField()
    lyrics = serializers.CharField(required=False)
    genre = serializers.CharField(max_length=50, required=False)
    language = serializers.CharField(max_length=50, required=False)
    release_date = serializers.DateField(required=False) 