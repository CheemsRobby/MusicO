from celery import shared_task
from django.db.models import Count, Avg
from django.utils import timezone
from .models import (
    UserSimilarity, SongSimilarity, UserRecommendation,
    SongFeature, UserPreference, RecommendationTask
)
from apps.music.models import Song
from apps.user.models import User
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

@shared_task
def calculate_user_similarities():
    """计算用户相似度"""
    users = User.objects.all()
    user_ratings = {}
    
    # 收集用户评分数据
    for user in users:
        ratings = user.ratings.all()
        user_ratings[user.id] = {
            rating.song_id: rating.rating
            for rating in ratings
        }
    
    # 计算用户相似度矩阵
    user_ids = list(user_ratings.keys())
    similarity_matrix = np.zeros((len(user_ids), len(user_ids)))
    
    for i, user1_id in enumerate(user_ids):
        for j, user2_id in enumerate(user_ids):
            if i < j:
                # 计算两个用户的共同评分歌曲
                common_songs = set(user_ratings[user1_id].keys()) & set(user_ratings[user2_id].keys())
                if common_songs:
                    # 计算余弦相似度
                    user1_ratings = [user_ratings[user1_id][song_id] for song_id in common_songs]
                    user2_ratings = [user_ratings[user2_id][song_id] for song_id in common_songs]
                    similarity = cosine_similarity([user1_ratings], [user2_ratings])[0][0]
                    similarity_matrix[i][j] = similarity
                    similarity_matrix[j][i] = similarity
    
    # 保存用户相似度
    for i, user1_id in enumerate(user_ids):
        for j, user2_id in enumerate(user_ids):
            if i != j and similarity_matrix[i][j] > 0:
                UserSimilarity.objects.update_or_create(
                    user_id=user1_id,
                    similar_user_id=user2_id,
                    defaults={'similarity_score': similarity_matrix[i][j]}
                )

@shared_task
def calculate_song_similarities():
    """计算歌曲相似度"""
    songs = Song.objects.all()
    song_features = {}
    
    # 收集歌曲特征数据
    for song in songs:
        try:
            features = song.features
            song_features[song.id] = [
                features.tempo, features.energy, features.danceability,
                features.valence, features.acousticness, features.instrumentalness,
                features.liveness, features.speechiness
            ]
        except SongFeature.DoesNotExist:
            continue
    
    # 标准化特征
    feature_matrix = np.array(list(song_features.values()))
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(feature_matrix)
    
    # 计算歌曲相似度矩阵
    song_ids = list(song_features.keys())
    similarity_matrix = cosine_similarity(normalized_features)
    
    # 保存歌曲相似度
    for i, song1_id in enumerate(song_ids):
        for j, song2_id in enumerate(song_ids):
            if i != j and similarity_matrix[i][j] > 0:
                SongSimilarity.objects.update_or_create(
                    song_id=song1_id,
                    similar_song_id=song2_id,
                    defaults={'similarity_score': similarity_matrix[i][j]}
                )

@shared_task
def generate_recommendations(user_id, recommendation_type='hybrid', limit=10, use_preferences=True):
    """生成推荐"""
    user = User.objects.get(id=user_id)
    task = RecommendationTask.objects.create(
        user=user,
        task_type=recommendation_type,
        status='processing'
    )
    
    try:
        recommendations = []
        
        if recommendation_type == 'collaborative':
            # 基于协同过滤的推荐
            similar_users = UserSimilarity.objects.filter(
                user=user
            ).order_by('-similarity_score')[:5]
            
            for similar_user in similar_users:
                # 获取相似用户喜欢但当前用户未听过的歌曲
                similar_user_ratings = similar_user.similar_user.ratings.filter(
                    rating__gte=4
                ).exclude(song__in=user.ratings.values_list('song', flat=True))
                
                for rating in similar_user_ratings:
                    score = rating.rating * similar_user.similarity_score
                    recommendations.append({
                        'song': rating.song,
                        'score': score,
                        'type': 'collaborative',
                        'explanation': f'Similar user {similar_user.similar_user.username} rated this song {rating.rating} stars'
                    })
        
        elif recommendation_type == 'content':
            # 基于内容的推荐
            user_ratings = user.ratings.filter(rating__gte=4)
            for rating in user_ratings:
                similar_songs = SongSimilarity.objects.filter(
                    song=rating.song
                ).order_by('-similarity_score')[:5]
                
                for similar_song in similar_songs:
                    if not user.ratings.filter(song=similar_song.similar_song).exists():
                        score = rating.rating * similar_song.similarity_score
                        recommendations.append({
                            'song': similar_song.similar_song,
                            'score': score,
                            'type': 'content',
                            'explanation': f'Similar to {rating.song.title} which you rated {rating.rating} stars'
                        })
        
        elif recommendation_type == 'hybrid':
            # 混合推荐
            collaborative_recommendations = generate_recommendations(
                user_id, 'collaborative', limit, use_preferences
            )
            content_recommendations = generate_recommendations(
                user_id, 'content', limit, use_preferences
            )
            
            # 合并推荐结果
            recommendations = collaborative_recommendations + content_recommendations
            
        else:  # popular
            # 热门推荐
            popular_songs = Song.objects.annotate(
                avg_rating=Avg('ratings__rating'),
                rating_count=Count('ratings')
            ).filter(
                avg_rating__gte=4,
                rating_count__gte=10
            ).exclude(
                id__in=user.ratings.values_list('song', flat=True)
            ).order_by('-avg_rating', '-rating_count')[:limit]
            
            for song in popular_songs:
                recommendations.append({
                    'song': song,
                    'score': song.avg_rating,
                    'type': 'popular',
                    'explanation': f'Popular song with average rating of {song.avg_rating:.1f} from {song.rating_count} ratings'
                })
        
        # 应用用户偏好过滤
        if use_preferences:
            try:
                preferences = user.preferences
                filtered_recommendations = []
                
                for rec in recommendations:
                    song = rec['song']
                    include = True
                    
                    # 检查流派偏好
                    if preferences.preferred_genres and song.genre not in preferences.preferred_genres:
                        include = False
                    
                    # 检查艺术家偏好
                    if preferences.preferred_artists and song.artist.id not in preferences.preferred_artists:
                        include = False
                    
                    # 检查年代偏好
                    if preferences.preferred_decades and song.release_date:
                        decade = (song.release_date.year // 10) * 10
                        if decade not in preferences.preferred_decades:
                            include = False
                    
                    if include:
                        filtered_recommendations.append(rec)
                
                recommendations = filtered_recommendations
            except UserPreference.DoesNotExist:
                pass
        
        # 按分数排序并限制数量
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        recommendations = recommendations[:limit]
        
        # 保存推荐结果
        for rec in recommendations:
            UserRecommendation.objects.update_or_create(
                user=user,
                song=rec['song'],
                defaults={
                    'recommendation_type': rec['type'],
                    'score': rec['score']
                }
            )
        
        task.status = 'completed'
        task.result = {
            'recommendations': [
                {
                    'song_id': rec['song'].id,
                    'score': rec['score'],
                    'type': rec['type'],
                    'explanation': rec.get('explanation', '')
                }
                for rec in recommendations
            ]
        }
        task.save()
        
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.save()
        raise 