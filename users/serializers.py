from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, data):
        data['password'] = make_password(data['password'])
        username = f"{data['first_name']}.{data['last_name']}"
        duplicates = User.objects.filter(first_name=data['first_name'],
                                        last_name=data['last_name']).all()
        if duplicates:
            username += str(len(duplicates))
        data['username'] = username
        data.pop('confirm_password')
        return super(UserSerializer, self).create(data)

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("El e-mail ya se encuentra en uso")
        return email

    def validate(self, data):
        data.setdefault('first_name', None)
        data.setdefault('last_name', None)
        data.setdefault('password', None)
        data.setdefault('confirm_password', None)

        if None in data.values():
            raise serializers.ValidationError("Faltan datos para el registro")

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True,
                                source='get_user_token')
    class Meta:
        model = User
        exclude = [
            'password',
        ]