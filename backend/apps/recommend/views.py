from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import (
    UserSimilarity, SongSimilarity, UserRecommendation,
    SongFeature, UserPreference, RecommendationTask
)
from .serializers import (
    UserSimilaritySerializer, SongSimilaritySerializer,
    UserRecommendationSerializer, SongFeatureSerializer,
    UserPreferenceSerializer, RecommendationTaskSerializer,
    RecommendationRequestSerializer
)
from apps.music.models import Song
from apps.user.models import User
from .tasks import (
    calculate_user_similarities,
    calculate_song_similarities,
    generate_recommendations
)

class UserSimilarityViewSet(viewsets.ModelViewSet):
    queryset = UserSimilarity.objects.all()
    serializer_class = UserSimilaritySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """触发用户相似度计算"""
        task = calculate_user_similarities.delay()
        return Response({'task_id': task.id})

class SongSimilarityViewSet(viewsets.ModelViewSet):
    queryset = SongSimilarity.objects.all()
    serializer_class = SongSimilaritySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        song_id = self.request.query_params.get('song_id')
        if song_id:
            return self.queryset.filter(song_id=song_id)
        return self.queryset.none()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """触发歌曲相似度计算"""
        task = calculate_song_similarities.delay()
        return Response({'task_id': task.id})

class UserRecommendationViewSet(viewsets.ModelViewSet):
    queryset = UserRecommendation.objects.all()
    serializer_class = UserRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        """请求新的推荐"""
        serializer = RecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # 检查是否需要刷新推荐
            if data['refresh']:
                task = generate_recommendations.delay(
                    user_id=request.user.id,
                    recommendation_type=data['recommendation_type'],
                    limit=data['limit'],
                    use_preferences=data['use_preferences']
                )
                return Response({'task_id': task.id})
            
            # 返回现有的推荐
            recommendations = self.get_queryset().filter(
                recommendation_type=data['recommendation_type']
            ).order_by('-score')[:data['limit']]
            
            if not recommendations and data['recommendation_type'] != 'popular':
                # 如果没有推荐，生成新的
                task = generate_recommendations.delay(
                    user_id=request.user.id,
                    recommendation_type=data['recommendation_type'],
                    limit=data['limit'],
                    use_preferences=data['use_preferences']
                )
                return Response({'task_id': task.id})
            
            serializer = self.get_serializer(recommendations, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongFeatureViewSet(viewsets.ModelViewSet):
    queryset = SongFeature.objects.all()
    serializer_class = SongFeatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        song_id = self.request.query_params.get('song_id')
        if song_id:
            return self.queryset.filter(song_id=song_id)
        return self.queryset.none()

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        """创建或更新用户偏好"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            preference, created = UserPreference.objects.update_or_create(
                user=request.user,
                defaults=serializer.validated_data
            )
            return Response(self.get_serializer(preference).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommendationTaskViewSet(viewsets.ModelViewSet):
    queryset = RecommendationTask.objects.all()
    serializer_class = RecommendationTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, pk=None):
        """获取任务状态和结果"""
        task = self.get_object()
        if task.status == 'completed':
            return Response({
                'status': task.status,
                'result': task.result
            })
        return Response({'status': task.status}) 