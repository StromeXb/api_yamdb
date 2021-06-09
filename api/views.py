from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import CustomUser
from .permissions import (IsAdmin, IsSuperuser)
from .serializers import UserSerializer


class UsersViewSet(ModelViewSet):
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
