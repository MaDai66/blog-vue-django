from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, FollowSerializer, UserProfileSerializer
from .models import Follow
from django.contrib.auth.models import User
from article.models import Article
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# 注册接口
class RegisterAPIView(APIView):
    def post(self,request):
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           
           return Response({'code':200,'message':'注册成功'})
       else:
           error_messages = []
           for field, errors in serializer.errors.items():
               for error in errors:
                   error_messages.append(error)
           return Response({'code':400,'message':'注册失败，请检查名字长度与密码长度是否符合要求','errors':error_messages},status=status.HTTP_400_BAD_REQUEST)

# 关注接口
class FollowAPIView(APIView):
    def post(self, request):
        """关注用户"""
        follower_id = request.data.get('follower_id')
        followed_id = request.data.get('followed_id')
        
        if not follower_id or not followed_id:
            return Response({'code':400,'message':'缺少必要参数'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            follower = User.objects.get(id=follower_id)
            followed = User.objects.get(id=followed_id)
        except User.DoesNotExist:
            return Response({'code':404,'message':'用户不存在'},status=status.HTTP_404_NOT_FOUND)
        
        if follower == followed:
            return Response({'code':400,'message':'不能关注自己'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            follow = Follow.objects.create(follower=follower, followed=followed)
            serializer = FollowSerializer(follow)
            return Response({'code':200,'message':'关注成功','data':serializer.data})
        except Exception as e:
            return Response({'code':400,'message':'已经关注过该用户'},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """取消关注"""
        follower_id = request.data.get('follower_id')
        followed_id = request.data.get('followed_id')
        
        if not follower_id or not followed_id:
            return Response({'code':400,'message':'缺少必要参数'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            follow = Follow.objects.get(follower_id=follower_id, followed_id=followed_id)
            follow.delete()
            return Response({'code':200,'message':'取消关注成功'})
        except Follow.DoesNotExist:
            return Response({'code':404,'message':'未关注该用户'},status=status.HTTP_404_NOT_FOUND)

# 关注列表接口
class FollowListAPIView(APIView):
    def get(self, request, user_id):
        """获取用户的关注列表"""
        try:
            user = User.objects.get(id=user_id)
            follows = user.following.all()
            serializer = FollowSerializer(follows, many=True)
            return Response({'code':200,'message':'获取关注列表成功','data':serializer.data})
        except User.DoesNotExist:
            return Response({'code':404,'message':'用户不存在'},status=status.HTTP_404_NOT_FOUND)

# 粉丝列表接口
class FollowerListAPIView(APIView):
    def get(self, request, user_id):
        """获取用户的粉丝列表"""
        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all()
            serializer = FollowSerializer(followers, many=True)
            return Response({'code':200,'message':'获取粉丝列表成功','data':serializer.data})
        except User.DoesNotExist:
            return Response({'code':404,'message':'用户不存在'},status=status.HTTP_404_NOT_FOUND)

# 用户信息接口
class UserProfileAPIView(APIView):
    def get(self, request, user_id):
        """获取用户信息"""
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response({'code':200,'message':'获取用户信息成功','data':serializer.data})
        except User.DoesNotExist:
            return Response({'code':404,'message':'用户不存在'},status=status.HTTP_404_NOT_FOUND)

# 统计用户关注信息
class UserStatsAPIView(APIView):
    def get(self, request, user_id):
        """获取用户粉丝数，关注数"""

        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all()
            following = user.following.all()
            articles_count = Article.objects.filter(author_id=user_id).count()

            return Response({'code':200,'message':'获取用户统计成功','data':{'followers':followers.count(),'following':following.count(),'articles':articles_count}})
        except User.DoesNotExist:
            return Response({'code':404,'message':'用户不存在'},status=status.HTTP_404_NOT_FOUND)

# 用户登出接口
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 对于前端应用，最简单的登出方式就是让前端删除本地存储的token
            # 后端不需要做任何复杂的处理
            return Response({'code': 200, 'message': '登出成功'})
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"登出失败详细错误: {error_detail}")
            return Response({
                'code': 500, 
                'message': '登出失败',
                'error': str(e),
                'error_detail': error_detail
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)