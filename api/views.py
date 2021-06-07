from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from django.contrib.auth import get_user_model

from .models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer, ConfirmationCodeTokenObtainSerializer
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenViewBase


@api_view(['POST'])
@permission_classes([BasePermission])
def generate_code(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user, created = User.objects.get_or_create(email=email)
            confirmation_code = default_token_generator.make_token(user)
        else:
            return Response(
                'Please provide email via "email" field',
                status=status.HTTP_403_FORBIDDEN
            )
        user.email_user(
            subject='confirmation_code',
            message=f'Your confirmation code is {confirmation_code}',
            from_email='vader@starwars.tat'
        )
        return Response({'confirmation_code': f'{confirmation_code}'})


class ConfirmationCodeTokenObtain(TokenViewBase):
    permission_classes = [BasePermission]
    serializer_class = ConfirmationCodeTokenObtainSerializer
