from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import json
# Create your views here.

@api_view(['POST'])
def login(req):
    LOGIN_ERROR = 'Credenciales inválidas'
    body = json.loads(req.body)

    username = body.get('username')
    password = body.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(LOGIN_ERROR+' 1')

    if not check_password(password, user.password):
        return Response(LOGIN_ERROR+' 2')

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})