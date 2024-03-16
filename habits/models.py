from django.db import models
from habits.validators import validate_execution_time, validate_reward_and_linked_habit, validate_linked_habit, \
    validate_rewarding_habit, validate_frequency
from telegram_utils import send_notification
from user.models import User


class Habit(models.Model):
    """
    Модель для управления привычками пользователя.
    Параметры:
    user (ForeignKey): Пользователь, создавший привычку.
    place (CharField): Место, в котором необходимо
    выполнять привычку.
    time (TimeField): Время, когда необходимо выполнять привычку.
    action (CharField): Действие,
    которое представляет собой привычку.
    is_rewardable (BooleanField): Признак того, что привычка вознаграждаема.
    related_habit (ForeignKey): Связанная привычка, если есть.
    frequency (IntegerField): Периодичность выполнения привычки для напоминания в днях.
    reward (CharField): Вознаграждение за выполнение привычки.
    execution_time (IntegerField): Время, которое предположительно потратит пользователь на выполнение привычки (в секундах).
    is_public (BooleanField): Признак публичности привычки.
    """
    title = models.CharField(max_length=100, verbose_name='название привычки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_rewardable = models.BooleanField(default=False, verbose_name='Вознаграждаемая привычка')
    related_habit = models.ForeignKey('self', validators=[validate_linked_habit], on_delete=models.CASCADE, null=True,
                                      blank=True,
                                      verbose_name='Связанная привычка')
    frequency = models.IntegerField(default=1, validators=[validate_frequency], verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вознаграждение')
    execution_time = models.IntegerField(default=120, validators=[validate_execution_time], verbose_name='Время '
                                                                                                         'выполнения (в секундах)')  # По умолчанию 120 секунд
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    def clean(self):
        if not self.action:
            raise ValueError("Действие должно быть указано")

        validate_reward_and_linked_habit({'reward': self.reward, 'linked_habit': self.related_habit})
        validate_rewarding_habit(self)

    def __str__(self):
        """
        Возвращает строковое представление привычки.
        """
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class HabitRecord(models.Model):
    """
    Модель для отслеживания выполнения привычек.
    Параметры:
    habit (ForeignKey): Привычка, для которой отслеживается выполнение.
    date (DateField): Дата выполнения привычки.
    completed (BooleanField): Признак выполнения привычки.
    """
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        verbose_name="Привычка"
    )
    date = models.DateField(verbose_name="Дата")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")

    def save(self, *args, **kwargs):
        # Переопределяем метод save для отправки уведомления при создании записи о выполнении привычки
        super().save(*args, **kwargs)
        # Отправляем уведомление
        send_notification(self.habit.owner.telegram_id, self.habit.action, self.habit.time)

    def __str__(self):
        """
        Возвращает строковое представление записи выполнения привычки.
        """
        return f"{self.habit.action} - {self.date}"
