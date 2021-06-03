from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Страница админ. панели произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('name', 'year', 'category',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Страница админ. панели жанров."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Страница админ. панели категорий."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
