from django.db import models
from django.core import validators
from users.models import User
from courses.models import Course

class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    #files

class Assignment(Post):
    due_datetime = models.DateTimeField()
    #files

class Homework(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='homeworks')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    turn_in_timestamp = models.DateTimeField(auto_now=True)
    grade = models.IntegerField(
        validators=[
            validators.MaxValueValidator(20),
            validators.MinValueValidator(0)
        ]
    )
    #weight
    #files