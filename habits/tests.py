from django.test import TestCase
from user.models import User
from .models import Habit


class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.habit_data = {
            'place': 'Home',
            'time': '08:00',
            'action': '',  # Установим action пустым
            'is_rewardable': True,
            'frequency': 1,
            'reward': 'Coffee',
            'execution_time': 120,
            'is_public': True,
        }

    def test_habit_validation(self):
        # Попытаемся создать привычку с пустым action
        with self.assertRaises(ValueError):
            habit = Habit.objects.create(user=self.user, **self.habit_data)
            habit.full_clean()


class HabitAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.habit_data = {
            'place': 'Home',
            'time': '08:00',
            'action': 'Morning exercise',
            'is_rewardable': True,
            'frequency': 1,
            'reward': 'Coffee',
            'execution_time': 120,
            'is_public': True,
        }

    def test_create_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        self.assertEqual(habit.user, self.user)
        self.assertEqual(Habit.objects.count(), 1)

    def test_get_habit_list(self):
        Habit.objects.create(user=self.user, **self.habit_data)
        habits = Habit.objects.filter(user=self.user)
        self.assertEqual(habits.count(), 1)

    def test_get_habit_detail(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        fetched_habit = Habit.objects.get(pk=habit.pk)
        self.assertEqual(habit, fetched_habit)

    def test_update_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        updated_data = self.habit_data.copy()
        updated_data['place'] = 'Gym'
        habit.place = 'Gym'
        habit.save()
        self.assertEqual(habit.place, 'Gym')

    def test_delete_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        habit.delete()
        self.assertEqual(Habit.objects.count(), 0)
