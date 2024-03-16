from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user.models import User


class HabitAPITests(APITestCase):
    def setUp(self):
        # Создаем пользователя для аутентификации
        self.user = User.objects.create(email='testuser@test.com', password='12345')

    def test_habit_list_authenticated(self):
        # Аутентификация пользователя
        url_login = reverse('user:user-login')
        data_login = {'email': 'testuser@test.com', 'password': '12345'}
        response_login = self.client.post(url_login, data_login)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        # Получение токена доступа
        access_token = response_login.data['access']

        # Установка токена доступа для последующих запросов
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(access_token))

        # Запрос на получение списка привычек
        url_habit_list = reverse('habit-list')
        response_habit_list = self.client.get(url_habit_list)
        self.assertEqual(response_habit_list.status_code, status.HTTP_200_OK)

    def test_habit_list_unauthenticated(self):
        # Тест получения списка привычек без аутентификации
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_authentication(self):
        # Создаем пользователя с хешированным паролем для успешной аутентификации
        hashed_password = make_password('12345')
        user = User.objects.create(email='testuser2@test.com', password=hashed_password)

        # Попытка аутентификации
        url_login = reverse('user:user-login')
        data_login = {'email': 'testuser2@test.com', 'password': '12345'}
        response_login = self.client.post(url_login, data_login)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

    def test_habit_create_authenticated(self):
        # Аутентификация пользователя
        url_login = reverse('user:user-login')
        data_login = {'email': 'testuser@test.com', 'password': '12345'}
        response_login = self.client.post(url_login, data_login)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        token = response_login.data['access']

        # Установка токена доступа для последующих запросов
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Создание привычки
        url_create_habit = reverse('habit-create')
        data_create_habit = {'name': 'Test Habit'}
        response_create_habit = self.client.post(url_create_habit, data_create_habit)
        self.assertEqual(response_create_habit.status_code, status.HTTP_201_CREATED)

    def test_habit_create_unauthenticated(self):
        # Тест создания привычки без аутентификации
        url = reverse('habit-create')
        data = {'name': 'Test Habit'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
