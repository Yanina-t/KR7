from django.db import models

# reminders/models.py
from django.db import models
from user.models import User
from habits.models import Habit


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ScheduledReminder(models.Model):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

