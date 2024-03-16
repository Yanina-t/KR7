from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Habit
from .pagination import HabitListPagination
from .serializers import HabitCreateSerializer, HabitReadSerializer
from habits.permissions import IsPublicReadOnly, IsOwnerOrReadOnly

User = get_user_model()


class HabitListAPIView(generics.ListCreateAPIView):
    """
    Представление для получения списка привычек и создания новой привычки.
    """
    serializer_class = HabitReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitListPagination

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Получаем список привычек текущего пользователя и публичных привычек
        queryset = Habit.objects.filter(owner=user) | Habit.objects.filter(is_public=True)

        return queryset.order_by('id')  # Упорядочить по идентификатору

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как владельца привычки
        serializer.save(owner=self.request.user)


class HabitCreateView(generics.CreateAPIView):
    """
    Представление для создания новой привычки.
    """
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]  # Обеспечиваем, что пользователь аутентифицирован
    pagination_class = HabitListPagination

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как владельца привычки
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        # Вызываем метод create из CreateAPIView
        response = super().post(request, *args, **kwargs)
        # Проверяем успешность создания привычки
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'Привычка успешно создана'}, status=status.HTTP_201_CREATED)
        return response


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitReadSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitListPagination

    def perform_update(self, serializer):
        # Убедимся, что только владелец привычки может ее обновлять
        if serializer.instance.owner == self.request.user:
            serializer.save()
        else:
            return Response({"error": "Вы не владелец привычки"}, status=status.HTTP_403_FORBIDDEN)


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Представление для получения списка публичных привычек.
    """
    serializer_class = HabitReadSerializer
    permission_classes = [IsPublicReadOnly]  # Кастомное разрешение доступа
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
