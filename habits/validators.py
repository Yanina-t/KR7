# habit/validators.py

from django.core.exceptions import ValidationError


def validate_reward_and_linked_habit(habit):
    if habit.reward or habit.related_habit is not None:
        raise ValidationError("Необходимо выбрать только одно из полей: вознаграждение или связанная привычка.")


def validate_execution_time(value):
    if value > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")


def validate_linked_habit(habit):
    if habit and not habit.is_rewardable:
        raise ValidationError("Связанная привычка должна быть приятной привычкой.")


def validate_rewarding_habit(habit):
    if habit.is_rewardable and (habit.reward or habit.related_habit):
        raise ValidationError("Для приятной привычки не должно быть указано вознаграждение или связанная привычка.")


def validate_frequency(value):
    if value < 7:
        raise ValidationError("Частота выполнения привычки не может быть реже 1 раза в 7 дней.")
