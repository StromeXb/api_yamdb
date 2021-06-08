# from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.aggregates import Avg
from django.contrib.auth.models import AbstractUser

# User = get_user_model()


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
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
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
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
