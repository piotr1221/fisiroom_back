from django.db import models
from django.core import validators
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    visual_config = models.IntegerField(
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(3)            
        ],
        default = 0
    )
    fontsize = models.IntegerField(
        validators=[
            validators.MinValueValidator(12),
            validators.MaxValueValidator(32)
        ],
        default = 16
    )
    cursorsize = models.IntegerField(
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(2)
        ],
        default = 0
    )
    
    def get_user_token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token