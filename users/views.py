from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from users.models import User
from django.contrib.auth.hashers import check_password
from . import serializers

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects

    def create(self, req):
        serializer = self.serializer_class(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, req):
        LOGIN_ERROR = {'message': 'Credenciales inválidas'}

        email = req.data.get('email', None)
        password = req.data.get('password', None)

        if email is None or password is None:
            return Response(LOGIN_ERROR, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(LOGIN_ERROR, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response(LOGIN_ERROR, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserLoginSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserGradeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserGradeSerializer
    queryset = serializer_class.Meta.model.objects

    def update(self, request, pk=None):
        queryset = self.queryset.filter()
        student = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(student, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
