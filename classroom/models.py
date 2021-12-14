from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    creation_timestamp = models.DateTimeField(auto_now=True)
    #files

class Assignment(Post):
    due_datetime = models.DateTimeField()
    pass

class Homework(models.Model):
    turn_in_timestamp = models.DateTimeField(auto_now=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    #files