from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import RefreshToken

from .models import Category, Comment, CustomUser, Genre, Review, Roles, Title


class ConfirmationCodeTokenObtainSerializer(serializers.Serializer):

    email_field = CustomUser.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.email_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):

        user = get_object_or_404(CustomUser, email=attrs[self.email_field])
        check_token = default_token_generator.check_token(
            user, attrs['confirmation_code']
        )

        if not check_token:
            raise AuthenticationFailed(
                self.error_messages['confirmation_code'],
                'confirmation_code is not valid',
            )

        data = {}
        refresh = self.get_token(user)

        data['access'] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=Roles.USER)

    class Meta:

        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        exclude = ('id', )
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
        slug_field='slug', queryset=Category.objects.all(), many=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = ('__all__')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецензий
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs['title_id']
            if Review.objects.filter(
                author=author, title__id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Title already has your review.'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        model = Comment
