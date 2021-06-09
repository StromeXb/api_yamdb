from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True,
                              blank=False, null=False)
    bio = models.CharField(max_length=4000, null=True)
    role = models.CharField(max_length=50, choices=Roles.choices)

    @property
    def is_admin(self):
        return self.is_staff or self.role == Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR
