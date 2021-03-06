from django.db import models
from django.core import validators
from users.models import User
from courses.models import Course

# Problema de consistencia con respecto a la id para la entidad de la base de datos y 
# la id para guardar los archivos relacionados en el bucket

# Problemas al guiarse la futura id de un post para guardarla dentro del bucket de imagenes
# Al ser calculada mediante la longitud de las instancias, ante posibles eliminaciones de registros de la tabla Post
# causaria problemas de conflicto de llaves de los post para el guardado de archivos en el bucket 

def post_storage_path(instance, filename):
    id = len(Post.objects.filter(course=instance.course)) + 1
    return f'{instance.course.get_storage_path()}/posts/{id}/{filename}'

################################################################################################

class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=post_storage_path, null=True, blank=True)

    def get_storage_path(self):
        return f'{self.course.get_storage_path()}/posts/{self.pk}'

class Assignment(Post):
    due_datetime = models.DateTimeField()


def homework_storage_path(instance, filename):
    id = len(Homework.objects.filter(assignment=instance.assignment)) + 1
    return f'{instance.assignment.get_storage_path()}/homeworks/{id}/{filename}'

class Homework(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='homeworks')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    turn_in_timestamp = models.DateTimeField(auto_now=True)
    grade = models.IntegerField(
        validators=[
            validators.MaxValueValidator(20),
            validators.MinValueValidator(0)
        ],
        default = 0
    )
    file = models.FileField(upload_to=homework_storage_path, null=True, blank=True)
    # weight

    def get_storage_path(self):
        return f'{self.assignment.get_storage_path()}/homeworks/{self.pk}'
