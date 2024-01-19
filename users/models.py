from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import NULLABLE


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    auth_guid_code = models.CharField(max_length=36, verbose_name='код', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        permissions = [
            (
                'set_active',
                'Возможно отключить пользователя'
            )
        ]
