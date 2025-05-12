from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.user.urls')),
    path('api/music/', include('apps.music.urls')),
    path('api/recommend/', include('apps.recommend.urls')),
    path('api/search/', include('apps.search.urls')),
    path('api/social/', include('apps.social.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 