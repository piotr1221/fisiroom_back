from rest_framework import serializers
from courses.models import Course
from courses.serializers import CourseCardSerializer
from users.serializers import UserSerializer
import time
from users.models import User
from . import models

class ClassroomHomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Homework
        fields = '__all__'

class ClassroomPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = '__all__'


class ClassroomCourseSerializer(CourseCardSerializer):
    enrolled = UserSerializer(many=True, read_only=True)
    posts = ClassroomPostSerializer(many=True, read_only=True)
    owner = serializers.CharField(source='owner.id', required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, data):
        data['owner'] = self.context['owner']
        return super(ClassroomCourseSerializer, self).create(data)

    def validate(self, data):
        data.setdefault('title', None)
        data.setdefault('description', None)
        data.setdefault('day', None)
        data.setdefault('time_start', None)
        data.setdefault('time_end', None)

        if None in data.values():
            return serializers.ValidationError("Faltan datos para el registro")

        if data['day'] not in [str(i) for i in range(1, 7+1)]:
            return serializers.ValidationError("Dia fuera de rango")

        if not data['time_start'] < data['time_end']:
            return serializers.ValidationError("Horario inconsistente")

        return data