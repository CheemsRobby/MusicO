from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserUpdateView,
    PasswordChangeView,
    UserProfileUpdateView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('preferences/', UserProfileUpdateView.as_view(), name='preferences'),
] 