from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EmailUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    ''' 用户序列化器 '''
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(
        max_length=100, min_length=10, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email",
                  "created_at", "updated_at"]

    def validate(self, attrs):
        email = attrs.get('eamil')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "email is already in user table"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if not user:
            raise serializers.ValidationError(
                {"email": "email is not in user table"})
        user.password = make_password(validated_data['password'])
        user.save()
        return user


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
