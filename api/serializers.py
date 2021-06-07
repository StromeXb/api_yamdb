from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Review, Comment, Title

User = get_user_model()


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


from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

class ConfirmationCodeTokenObtainSerializer(serializers.Serializer):

    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confirmation_code': attrs['confirmation_code'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        user = get_object_or_404(User, email=attrs[self.username_field])
        check_token = default_token_generator.check_token(user, attrs['confirmation_code'])

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
    """
    Сериализатор для пользователей
    """

    class Meta:
        fields = '__all__'
        model = get_user_model()
