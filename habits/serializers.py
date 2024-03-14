from rest_framework import serializers

from .models import Habit


class HabitCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новой привычки.
    """
    class Meta:
        model = Habit
        exclude = ['owner']


class HabitReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации о привычке.
    """
    class Meta:
        model = Habit
        fields = '__all__'