from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def get_user_token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token