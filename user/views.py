from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, MyTokenObtainPairSerializer
from .utils import send_registration_confirmation_email
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    Представление для управления пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserRegistrationAPIView(CreateAPIView):
    """
    Представление для регистрации новых пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        """
        Создание нового пользователя.
        """
        user = serializer.save()
        user.is_active = True
        user.save()
        # Отправка письма с подтверждением регистрации
        send_registration_confirmation_email(user.email)


class UserLoginAPIView(TokenObtainPairView):
    """
    Представление для аутентификации пользователей и получения JWT токенов.
    """
    serializer_class = MyTokenObtainPairSerializer
