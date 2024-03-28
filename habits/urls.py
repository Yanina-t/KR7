from django.urls import path
from .views import (
    HabitListAPIView,
    HabitCreateView,
    HabitDetailView, PublicHabitListAPIView,
)

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('public-habits/', PublicHabitListAPIView.as_view(), name='public_habits_list'),
]
