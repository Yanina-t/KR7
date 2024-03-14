from django.shortcuts import render

# reminders/views.py
from django.http import JsonResponse


def handle_telegram_webhook(request):
    # Обработка запросов от телеграмма здесь
    # Разбор полученных сообщений и отправка соответствующих ответов
    return JsonResponse({'status': 'ok'})

