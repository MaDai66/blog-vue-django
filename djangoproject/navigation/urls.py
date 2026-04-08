from django.urls import path
from .views import GetNavigationAPIView
app_name = 'article'
urlpatterns = [
    path('get', GetNavigationAPIView.as_view(), name='get_navigation'),
]