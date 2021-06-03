import uuid

from django.contrib.auth.models import AbstractUser

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.aggregates import Avg

# User = get_user_model()


class ManualUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=100,
        choices=Role.choices,
        default=Role.USER,
    )

    @property
    def is_admin(self):
        return self.is_superuser or (self.role == self.Role.ADMIN)

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        if self.username:
            name = f'{self.username}:{self.email}'
        else:
            name = self.email
        return name


class Title(models.Model):
    # Часть Ани

    @property
    def rating(self):
        rating = self.reviews.aggregate(Avg('score'))
        if rating:
            return rating
        return None


class Review(models.Model):
    """
    Класс описывает модель для отзывов
    """
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        ManualUser, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='1 review per title by user'
            ),
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    """
    Класс описывает комментарии к рецензиям
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        ManualUser, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
