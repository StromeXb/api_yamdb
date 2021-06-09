from django.urls import path
from .views import auth_send_email, auth_token

auth_url_patterns = [
    path('email/', auth_send_email, name='auth_send_email'),
    path('token/', auth_token, name='auth_token'),
]