from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from . import serializers
# Create your views here.

@api_view(['POST'])
def login(req):
    LOGIN_ERROR = {'message': 'Credenciales inválidas'}

    email = req.data.get('email', None)
    password = req.data.get('password', None)

    if email == None or password == None:
        return Response(LOGIN_ERROR)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(LOGIN_ERROR)

    if not check_password(password, user.password):
        return Response(LOGIN_ERROR)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializers.UserSerializer.Meta.model.objects.filter(is_active=1)

    def get_queryset(self, pk=None):
        if pk is None:
            return serializers.UserSerializer.Meta.model.objects.filter(is_active=1).all()
        return serializers.UserSerializer.Meta.model.objects.filter(id=pk, is_active=1).first()

    def create(self, req):
        serializer = serializers.UserRegistrationSerializer(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.UserSerializer(data=serializer.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'message': 'Usuario registrado con exito'}, status=status.HTTP_201_CREATED)
