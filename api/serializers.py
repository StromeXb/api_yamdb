from rest_framework import serializers

from .models import Review, Comment, Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецензий
    """
    author = serializers.SlugField(read_only=True, slug_field='username')

    class Meta:
        exclude = ('title', )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """
    author = serializers.SlugField(read_only=True, slug_field='username')

    class Meta:
        exclude = ('review',)
        model = Comment
