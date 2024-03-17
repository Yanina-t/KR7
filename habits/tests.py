from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.core.exceptions import ValidationError
from habits.validators import (
    validate_reward_and_linked_habit,
    validate_execution_time,
    validate_linked_habit,
    validate_rewarding_habit,
    validate_frequency
)
from django.test import TestCase
from django.urls import reverse
from habits.pagination import HabitListPagination
from habits.models import Habit
from user.models import User
from django.test import RequestFactory
from rest_framework.request import Request

from user.permissions import IsAdminOrReadOnly


class HabitModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='12345')

    def test_clean_without_action(self):
        # Создаем экземпляр Habit без указания действия
        habit = Habit.objects.create(
            title='Test Habit',
            owner=self.user,
            place='Test Place',
            time='10:50',
            action=''  # Пустое действие
        )

        # Метод clean должен вызывать исключение ValueError
        with self.assertRaises(ValueError):
            habit.clean()

    def test_clean_with_invalid_reward_and_linked_habit(self):
        # Создаем экземпляр Habit с некорректными данными
        habit = Habit.objects.create(
            title='Test Habit',
            owner=self.user,
            place='Test Place',
            time='10:50',
            action='Test Action',
            reward='Invalid Reward',  # Некорректное вознаграждение
            related_habit=None   # Установим связанную привычку в None
        )

        # Метод clean должен вызывать исключение ValidationError
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_clean_with_valid_reward_and_linked_habit(self):
        # Создаем экземпляр Habit с корректными данными
        habit = Habit.objects.create(
            title='Test Habit',
            owner=self.user,
            place='Test Place',
            time='10:50',
            action='Test Action',
            reward=None,  # Установим вознаграждение в None
            related_habit=None  # Нет связанной привычки
        )

        # Метод clean должен быть выполнен без ошибок
        habit.clean()


class HabitAPITests(APITestCase):
    def setUp(self):
        # Создаем пользователя для аутентификации
        self.user = User.objects.create(email='testuser@test.com', password='12345')
        # Создаем привычку для тестирования
        self.habit = Habit.objects.create(
            title='Test Habit',
            place='Test Place',
            time='14:40',
            action='Test Action',
            owner=self.user
        )

    def test_habit_list_authenticated(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос на получение списка привычек
        url_habit_list = reverse('habit-list')
        response_habit_list = self.client.get(url_habit_list)

        # Проверка статус кода ответа
        self.assertEqual(response_habit_list.status_code, status.HTTP_200_OK)

    def test_habit_list_unauthenticated(self):
        # Запрос списка привычек без аутентификации
        url_habit_list = reverse('habit-list')
        response_habit_list = self.client.get(url_habit_list)

        # Проверка статус кода ответа
        self.assertEqual(response_habit_list.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_create_authenticated(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Создание привычки
        url_create_habit = reverse('habit-create')
        data_create_habit = {
            "title": "test title1",
            "place": "test place1",
            "time": "14:41",
            "action": "test action1",

        }
        response_create_habit = self.client.post(url_create_habit, data_create_habit)
        # Проверка статус кода ответа
        self.assertEqual(response_create_habit.status_code, status.HTTP_201_CREATED)

    def test_habit_create_unauthenticated(self):
        # Создание привычки без аутентификации
        url_create_habit = reverse('habit-create')
        data_create_habit = {
            "title": "test title",
            "place": "test place",
            "time": "14:40",
            "action": "test action",
        }
        response_create_habit = self.client.post(url_create_habit, data_create_habit)

        # Проверка статус кода ответа
        self.assertEqual(response_create_habit.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_update_authenticated(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Обновление информации о привычке
        url_update_habit = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        data_update_habit = {
            "title": "Updated Test Title",
            "place": "Updated Test Place",
            "time": "15:00",
            "action": "Updated Test Action",
            "owner": self.user.id
        }
        response_update_habit = self.client.put(url_update_habit, data_update_habit)
        # Проверка статус кода ответа
        self.assertEqual(response_update_habit.status_code, status.HTTP_200_OK)
        # Обновляем данные привычки для проверки
        self.habit.refresh_from_db()
        # Проверка обновленных данных привычки
        self.assertEqual(self.habit.title, data_update_habit['title'])

    def test_habit_delete_authenticated(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Удаление привычки
        url_delete_habit = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        response_delete_habit = self.client.delete(url_delete_habit)

        # Проверка статус кода ответа
        self.assertEqual(response_delete_habit.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка удаления привычки из базы данных
        with self.assertRaises(Habit.DoesNotExist):
            self.habit.refresh_from_db()

    def test_habit_retrieve_unauthenticated(self):
        # Получение информации о привычке без аутентификации
        url_retrieve_habit = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        response_retrieve_habit = self.client.get(url_retrieve_habit)

        # Проверка статус кода ответа
        self.assertEqual(response_retrieve_habit.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_update_unauthenticated(self):
        # Обновление информации о привычке без аутентификации
        url_update_habit = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        data_update_habit = {
            "title": "Updated Test Title",
            "place": "Updated Test Place",
            "time": "15:00",
            "action": "Updated Test Action",
        }
        response_update_habit = self.client.put(url_update_habit, data_update_habit)

        # Проверка статус кода ответа
        self.assertEqual(response_update_habit.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_delete_unauthenticated(self):
        # Удаление привычки без аутентификации
        url_delete_habit = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        response_delete_habit = self.client.delete(url_delete_habit)

        # Проверка статус кода ответа
        self.assertEqual(response_delete_habit.status_code, status.HTTP_401_UNAUTHORIZED)


class ValidatorsTestCase(TestCase):
    def test_validate_reward_and_linked_habit(self):
        # Создаем фиктивный объект с атрибутами
        class FakeHabit:
            reward = 'test_reward'
            related_habit = 'test_linked_habit'

        # Проверяем, вызывается ли исключение при валидации
        with self.assertRaises(ValidationError):
            validate_reward_and_linked_habit(FakeHabit())

    def test_validate_execution_time(self):
        # Проверяем, вызывается ли исключение при времени выполнения более 120 секунд
        with self.assertRaises(ValidationError):
            validate_execution_time(121)

    def test_validate_linked_habit(self):
        # Создаем фиктивный объект с атрибутом is_rewardable
        class FakeLinkedHabit:
            is_rewardable = False

        # Проверяем, вызывается ли исключение при валидации
        with self.assertRaises(ValidationError):
            validate_linked_habit(FakeLinkedHabit())

    def test_validate_rewarding_habit(self):
        # Создаем фиктивный объект с атрибутами is_rewardable, reward и related_habit
        class FakeRewardingHabit:
            is_rewardable = True
            reward = 'test_reward'
            related_habit = None

        # Проверяем, вызывается ли исключение при валидации
        with self.assertRaises(ValidationError):
            validate_rewarding_habit(FakeRewardingHabit())

        # Создаем фиктивный объект с атрибутами is_rewardable и related_habit
        class FakeRewardingHabitWithLinkedHabit:
            is_rewardable = True
            reward = None
            related_habit = 'test_linked_habit'

        # Проверяем, вызывается ли исключение при валидации
        with self.assertRaises(ValidationError):
            validate_rewarding_habit(FakeRewardingHabitWithLinkedHabit())

    def test_validate_frequency(self):
        # Проверяем, вызывается ли исключение при частоте выполнения менее 7 дней
        with self.assertRaises(ValidationError):
            validate_frequency(6)



class HabitListPaginationTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя для аутентификации
        self.user = User.objects.create(email='testuser@test.com', password='12345')

        # Создаем несколько привычек для тестирования
        habits = [
            Habit(title=f'Test Habit {i}', place=f'Place {i}', time='15:00', action=f'Action {i}', owner=self.user)
            for i in range(15)
        ]
        Habit.objects.bulk_create(habits)

    def test_pagination_default_page_size(self):
        # Создаем экземпляр пагинации
        pagination = HabitListPagination()

        # Создаем запрос с пагинацией
        request = Request(RequestFactory().get(reverse('habit-list')))

        # Упорядочиваем QuerySet по полю 'id'
        queryset = Habit.objects.all().order_by('id')

        paginated_queryset = pagination.paginate_queryset(queryset, request)

        # Проверяем, что количество элементов на странице соответствует значению по умолчанию
        self.assertEqual(len(paginated_queryset), pagination.page_size)

    def test_pagination_custom_page_size(self):
        # Создаем экземпляр пагинации с кастомным размером страницы
        custom_page_size = 7
        pagination = HabitListPagination()
        pagination.page_size = custom_page_size

        # Создаем запрос с пагинацией
        request = Request(RequestFactory().get(reverse('habit-list')))

        # Упорядочиваем QuerySet по полю 'id'
        queryset = Habit.objects.all().order_by('id')

        paginated_queryset = pagination.paginate_queryset(queryset, request)

        # Проверяем, что количество элементов на странице соответствует кастомному размеру
        self.assertEqual(len(paginated_queryset), custom_page_size)
