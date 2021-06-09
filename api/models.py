from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# User = get_user_model()


class Genre(models.Model):
    """Класс описывает модель для жанра."""

    name = models.CharField('Название жанра', max_length=200)
    slug = models.SlugField('Уникальный адрес', unique=True)


class Category(models.Model):
    """Класс описывает модель для категории."""

    name = models.CharField('Название категории', max_length=200)
    slug = models.SlugField('Уникальный адрес', unique=True)


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

      
class Title(models.Model):
    """Класс описывает модель для произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=200,
        help_text='Введите название произведения'
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[MinValueValidator(1500), MaxValueValidator(2100)],
        help_text='Введите год выпуска произведения'
    )
    description = models.TextField(
        'Описание произведения',
        help_text='Введите описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        symmetrical=False,
        related_name='titles',
        verbose_name='Жанр публикации',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        """при печати объекта выводится название произведения."""

        return self.name

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

