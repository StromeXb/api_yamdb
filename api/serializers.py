from rest_framework import serializers

from .models import Roles, CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=Roles.USER)

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = CustomUser
