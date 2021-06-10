from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, ConfirmationCodeTokenObtain, GenreViewSet,
    ReviewViewSet, TitleViewSet, UsersViewSet, generate_code,
)

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews of title'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments of review'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', generate_code),
    path('v1/auth/token/', ConfirmationCodeTokenObtain.as_view())
]
