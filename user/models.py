from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', **NULLABLE)
    is_active = models.BooleanField(default=True)
    telegram_id = models.CharField(max_length=100, verbose_name='Телеграмм', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
