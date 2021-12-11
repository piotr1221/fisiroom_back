from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import json
# Create your views here.

@api_view(['POST'])
def login(req):
    LOGIN_ERROR = 'Credenciales inválidas'
    body = json.loads(req.body)

    email = body.get('email')
    password = body.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(LOGIN_ERROR)

    if not check_password(password, user.password):
        return Response(LOGIN_ERROR)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)