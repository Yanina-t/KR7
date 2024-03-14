# telegram_utils.py
import os
import requests
import telegram
from django.conf import settings


class MyBot:
    url = "https://api.telegram.org/bot"
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    def send_message(self, text):
        requests.post(
            url=f'{self.url}{self.token}/sendMessage',
            data={
                'chat_id': '485327994',  # Замените на нужный вам chat_id
                'text': text
            }
        )


def send_notification(chat_id, message):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=chat_id, text=message)
