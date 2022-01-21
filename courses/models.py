from django.db import models
from django.urls import reverse
from users.models import User
import uuid
# Create your models here.

def course_storage_path(instance, filename):
    id = len(Course.objects.all()) + 1
    return f'courses/{id}/{filename}'
class Course(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.FileField(upload_to=course_storage_path, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True, blank=True)
    DAY_CHOICES = [
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo')
    ]
    day = models.CharField(
        max_length=1,
        choices=DAY_CHOICES,
        default='1'
    )
    time_start = models.TimeField()
    time_end = models.TimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    enrolled = models.ManyToManyField(User, related_name='enrolled_courses')

    def __str__(self):
        return self.title

    def get_day_of_the_week(self):
        return self.DAY_CHOICES[int(self.day)-1][1]

    def get_owner_full_name(self):
        return self.owner.get_full_name()

    def get_absolute_url(self):
        return f'/classroom/{self.pk}'

    def get_storage_path(self):
        return f'courses/{self.pk}'