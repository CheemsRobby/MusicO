from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Artist, Album, Song, Playlist,
    PlaylistSong, UserListeningHistory, SongRating, Comment, Like
)
from .serializers import (
    ArtistSerializer, AlbumSerializer, SongSerializer,
    PlaylistSerializer, PlaylistSongSerializer,
    UserListeningHistorySerializer, SongRatingSerializer,
    SongUploadSerializer
)
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'bio']

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['artist', 'genre']
    search_fields = ['title', 'description']

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['artist', 'album', 'genre', 'language']
    search_fields = ['title', 'lyrics']

    def get_serializer_class(self):
        if self.action == 'upload':
            return SongUploadSerializer
        return SongSerializer

    @action(detail=True, methods=['post'])
    def play(self, request, pk=None):
        song = self.get_object()
        song.increment_play_count()
        
        # Record listening history
        UserListeningHistory.objects.create(
            user=request.user,
            song=song,
            duration=request.data.get('duration', 0)
        )
        
        return Response({'status': 'song played'})

    @action(detail=True, methods=['post'])
    def upload(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'is_public']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        order = request.data.get('order', playlist.songs.count() + 1)
        
        try:
            song = Song.objects.get(id=song_id)
            PlaylistSong.objects.create(
                playlist=playlist,
                song=song,
                order=order
            )
            return Response({'status': 'song added to playlist'})
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        
        try:
            playlist_song = PlaylistSong.objects.get(
                playlist=playlist,
                song_id=song_id
            )
            playlist_song.delete()
            return Response({'status': 'song removed from playlist'})
        except PlaylistSong.DoesNotExist:
            return Response(
                {'error': 'Song not found in playlist'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserListeningHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserListeningHistory.objects.all()
    serializer_class = UserListeningHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['song', 'device']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class SongRatingViewSet(viewsets.ModelViewSet):
    queryset = SongRating.objects.all()
    serializer_class = SongRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['song', 'rating']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@login_required
def player(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    comments = Comment.objects.filter(song=song).order_by('-created_at')
    
    # 获取歌词
    lyrics = []
    if song.lyrics_file:
        try:
            with open(song.lyrics_file.path, 'r', encoding='utf-8') as f:
                lyrics = f.read().split('\n')
        except:
            lyrics = ['暂无歌词']
    
    # 检查用户是否已收藏
    is_liked = Like.objects.filter(user=request.user, song=song).exists()
    
    context = {
        'song': song,
        'lyrics': lyrics,
        'comments': comments,
        'is_liked': is_liked
    }
    return render(request, 'player.html', context)

@login_required
def download_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    file_path = song.audio_file.path
    file_name = os.path.basename(file_path)
    
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

@require_POST
@login_required
def toggle_like(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    like, created = Like.objects.get_or_create(user=request.user, song=song)
    
    if not created:
        like.delete()
        return JsonResponse({'liked': False})
    
    return JsonResponse({'liked': True})

@require_POST
@login_required
def add_comment(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            user=request.user,
            song=song,
            content=content
        )
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'username': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': 0
            }
        })
    
    return JsonResponse({'success': False})

@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({'success': True, 'likes': comment.likes})

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def player(request):
    return render(request, 'player.html')

