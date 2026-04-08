from rest_framework.response import Response
from .serializers import ArticleSerializer, UserArticleSerializer
from rest_framework.views import APIView
from rest_framework import status, permissions, parsers
from .models import Article
from user.models import User 


# 获取⽂章视图类
class GetArticleAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        # 处理GET请求
        articles = Article.objects.all()
        serializer = UserArticleSerializer(articles, many=True)
        return Response({'code': 200, "data": serializer.data})

# 搜索⽂章视图类
class SearchArticleAPIView(APIView):
    def post(self, request):
    # 处理POST请求
        articles =Article.objects.filter(title__icontains=request.data.get('title'))
        serializer = ArticleSerializer(articles, many=True)
        return Response({'code': 200, "data": serializer.data})

# 发布⽂章视图类
class PublishArticleAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def post(self, request, *args, **kwargs):
        # 处理POST请求
        # 确保author_id设置为当前登录用户的ID
        data = request.data.copy()

        data['author_id'] = str(request.user.id)
        
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, "message": '发布成功'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 主页创建文章列表视图
class UserArticleAPIView(APIView):
    def get(self, request, author_id):
        # 处理GET请求
        articles = Article.objects.filter(author_id=author_id)
        serializer = UserArticleSerializer(articles, many=True)
        return Response({'code': 200, "data": serializer.data})
