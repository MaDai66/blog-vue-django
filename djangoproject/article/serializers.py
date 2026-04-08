from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

# 个人主页显示用户文章序列器
class UserArticleSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        try:
            user = User.objects.get(id=obj.author_id)
            return {
                'id': user.id,
                'username': user.username
            }

        except User.DoesNotExist:
            return None
    class Meta:
        model = Article
        fields = '__all__'