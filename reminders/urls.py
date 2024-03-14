# reminders/urls.py
from django.urls import path
from .views import handle_telegram_webhook


urlpatterns = [
    path('telegram_webhook/', handle_telegram_webhook, name='telegram_webhook'),
]
