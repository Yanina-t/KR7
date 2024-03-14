# habit/validators.py

from django.core.exceptions import ValidationError


def validate_reward_and_linked_habit(value):
    if value['reward'] and value['linked_habit']:
        raise ValidationError("Необходимо выбрать только одно из полей: вознаграждение или связанная привычка.")


def validate_execution_time(value):
    if value > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")


def validate_linked_habit(value):
    if value and not value.is_rewarding_habit:
        raise ValidationError("Связанная привычка должна быть приятной привычкой.")


def validate_rewarding_habit(value):
    if value.is_rewarding_habit and (value.reward or value.linked_habit):
        raise ValidationError("Для приятной привычки не должно быть указано вознаграждение или связанная привычка.")


def validate_frequency(value):
    if value < 7:
        raise ValidationError("Частота выполнения привычки не может быть реже 1 раза в 7 дней.")
