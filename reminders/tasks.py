import os

from celery import Celery
from datetime import datetime
from reminders.models import Habit
from telegram import Bot

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def send_habit_reminders():
    # Получаем текущее время
    now = datetime.now().time()

    # Получаем все привычки, которые нужно отправить в текущее время
    habits_to_send = Habit.objects.filter(time=now)

    # Отправляем каждую привычку
    for habit in habits_to_send:
        chat_id = habit.user.telegram_chat_id  # Получаем ID чата пользователя
        text = f"Напоминание о привычке: {habit.name}"  # Составляем текст сообщения
        send_message(chat_id, text)


def send_message(chat_id, text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)
