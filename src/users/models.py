from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    """
    Модель пользователя.
    """
    username = None
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        blank=False,
        null=False,
        unique=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
