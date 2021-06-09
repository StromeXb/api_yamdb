from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title, Roles, CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=Roles.USER)

    class Meta:

        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецензий
    """
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        exclude = ('title', )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        exclude = ('review',)
        model = Comment


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
