# utils.py
from django.core.mail import send_mail
import os
import requests


def send_registration_confirmation_email(user_email):
    subject = 'Подтверждение регистрации'
    message = 'Добро пожаловать! Ваш аккаунт успешно создан.'
    from_email = 'yaninatest3@gmail.com'  # Замените на свой адрес электронной почты
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


class MyBot:
    url = "https://api.telegram.org/bot"
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    def send_message(self, text):
        requests.post(
            url=f'{self.url}{self.token}/sendMessage',
            data={
                'chat_id': '485327994',
                'text': text
            }
        )
