from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationAPIView, UserLoginAPIView, UserViewSet
from user.apps import UserConfig

app_name = UserConfig.name

# Описание маршрутизации для ViewSet
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
] + router.urls
