from rest_framework import serializers
import re

from .models import Category, Comment, Genre, Review, Title, Roles, CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=Roles.USER)

    class Meta:

        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = '__all__'
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = '__all__'
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецензий
    """

    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = re.findall(
                r'titles/(?P<title_id>\d+)/reviews', self.context.get('request').path
            )[0]
            if Review.objects.filter(author=author, title__id=title_id).exists():
                raise serializers.ValidationError(
                    'Title already has your review.'
                )
        return attrs



class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """

    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        exclude = ('review',)
        model = Comment