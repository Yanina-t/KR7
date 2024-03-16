from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        """
        Создание нового пользователя.
        """
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор для получения пары токенов (обновляемого токена и доступа) при входе пользователя в систему.
    """

    @classmethod
    def get_token(cls, user):
        """
        Получение токена для пользователя.
        """
        token = super().get_token(user)
        # Добавление дополнительной информации в токен, если необходимо
        return token
