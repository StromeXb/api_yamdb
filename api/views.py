import django_filters.rest_framework

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .filters import TitleFilter
from .models import Category, CustomUser, Genre, Review, Title
from .permissions import (
    IsAdmin, IsAdminPermission, IsOwnerOrReadOnly, IsSuperuser,
)
from .serializers import (
    CategorySerializer, CommentSerializer,
    ConfirmationCodeTokenObtainSerializer, GenreSerializer, ReviewSerializer,
    TitleCreateSerializer, TitleSerializer, UserSerializer,
)
from .viewsets import ListCreateDestroyViewSet


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get', 'patch'],
            url_path='me')
    def me(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):

        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                id=self.kwargs.get('review_id'),
                title__id=self.kwargs.get('title_id')
            )
        )


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = [IsAdminPermission]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_code(request):
    """
    вью для отправки кода на почту
    """
    email = request.POST.get('email')
    if email:
        user, created = CustomUser.objects.get_or_create(email=email)
        confirmation_code = default_token_generator.make_token(user)
    else:
        return Response(
            'Please provide email via "email" field',
            status=status.HTTP_403_FORBIDDEN
        )
    user.email_user(
        subject='confirmation_code',
        message=f'Your confirmation code is {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER
    )
    return Response({'confirmation_code': f'{confirmation_code}'})


class ConfirmationCodeTokenObtain(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = ConfirmationCodeTokenObtainSerializer
