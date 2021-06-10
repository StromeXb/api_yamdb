from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_send_email(request):
    email_data = request.data
    email = email_data.get('email')
    if email:
        # сгенерировать username lolkek@gmail.com -> lolkek5g
        username = email.split('@')[0] + '5' + email.split('@')[1][0]
        # создать неактивного пользователя с этим email
        user_instance, created = User.get_or_create(email=email,
                                                    username=username)
        if created:
            user_instance.is_active = False
            user_instance.save()
        # привязать к нему конфирм код
        # отправить на почту конфирм код
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=422)

    confirmation_code = token_generator.make_token(user_object)


@api_view(['POST'])
def auth_token(request):
    # data = request.data
    pass
