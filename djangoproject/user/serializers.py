from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Follow


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=120,
       
        error_messages={
            'max_length': '用户名长度不能超过120个字符',
            
        }
    )
    password = serializers.CharField(
        write_only=True,
        max_length=120,
        min_length=6,
        error_messages={
            'max_length': '密码长度不能超过120个字符',
            'min_length': '密码长度不能少于6个字符'
        }
    )

    class Meta:
        model = User
        fields = ['id','username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user


class FollowSerializer(serializers.ModelSerializer):


    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
        read_only_fields = ['created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']