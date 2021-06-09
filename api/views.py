import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, CustomUser
from .permissions import IsAdminPermission, IsAdmin, IsSuperuser
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleCreateSerializer, TitleSerializer, UserSerializer
)

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
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    paginator_class = PageNumberPagination
    permission_classes = [IsAdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    paginator_class = PageNumberPagination
    permission_classes = [IsAdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    paginator_class = PageNumberPagination
    permission_classes = [IsAdminPermission]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == ('create' or 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer
