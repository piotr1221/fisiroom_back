from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'username',
            'first_name',
            'last_name'
        ]

    def create(self, data):
        data['password'] = make_password(data['password'])
        username = f"{data['first_name']}.{data['last_name']}"
        duplicates = User.objects.filter(first_name=data['first_name'],
                                        last_name=data['last_name']).all()
        if duplicates:
            username += str(len(duplicates))
        data['username'] = username
        return super(UserSerializer, self).create(data)

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("El e-mail ya se encuentra en uso")
        return email

    def validate(self, data):
        if not data['password'] or not data['confirm_password']:
            raise serializers.ValidationError("Ingrese su contraseña y su confirmación")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data