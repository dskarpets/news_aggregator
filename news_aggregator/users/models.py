from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Customized user model"""
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name='Фото профілю'
    )

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.username
