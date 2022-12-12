from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        return token


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=127)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data) -> User:
        if validated_data.pop("is_employee"):
            user = User.objects.create_superuser(**validated_data, is_employee=True)
            return user
        user = User.objects.create_user(**validated_data, is_employee=False)
        return user

    def validate_username(self, value) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken.")
        return value

    def validate_email(self, value) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered.")
        return value
