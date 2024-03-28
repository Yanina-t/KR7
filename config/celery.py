from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Поиск и загрузка задач из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()
