from django.urls import path
from .views import RegisterAPIView, FollowAPIView, FollowListAPIView, FollowerListAPIView, UserProfileAPIView, UserStatsAPIView, LogoutAPIView
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'user'
urlpatterns = [
    path('register',RegisterAPIView.as_view(),name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow', FollowAPIView.as_view(), name='follow'),
    path('follow/list/<int:user_id>', FollowListAPIView.as_view(), name='follow_list'),
    path('follower/list/<int:user_id>', FollowerListAPIView.as_view(), name='follower_list'),
    path('profile/<int:user_id>', UserProfileAPIView.as_view(), name='user_profile'),
    path('stats/<int:user_id>', UserStatsAPIView.as_view(), name='user_stats'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]