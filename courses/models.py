from django.db import models
from django.urls import reverse
from users.models import User
import uuid
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    icon = models.CharField(max_length=100, verbose_name='Icon', default='article')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('categories', arg=[self.slug])

    def __str__(self):
        return self.title

class Course(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #picture = models.ImageField(upload_to=user_directory_path)
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    enrolled = models.ManyToManyField(User, related_name='enrolled_courses')
    #questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

    def get_day_of_the_week(self):
        return self.DAY_CHOICES[int(self.day)-1][1]

    def get_owner_full_name(self):
        return self.owner.get_full_name()

    def get_absolute_url(self):
        return f'/classroom/{self.pk}'