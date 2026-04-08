from rest_framework.response import Response
from .serializers import NavigationSerializer
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import Navigation
# 获取导航栏视图类
class GetNavigationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        # 处理GET请求
        navigation = Navigation.objects.all() # 拿到所有导航
        serializer = NavigationSerializer(navigation, many=True)
        return Response({'code': 200, "data": serializer.data})