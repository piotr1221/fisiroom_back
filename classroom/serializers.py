from rest_framework import serializers
from courses.models import Course
from courses.serializers import CourseCardSerializer
from users.serializers import UserSerializer
import time
from users.models import User
from . import models
from rest_framework.response import Response

class ClassroomPostSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course.id', required=False)

    class Meta:
        model = models.Post
        fields = '__all__'

    def validate(self, data):
        data.setdefault('title', None)

        if None in data.values():
            raise serializers.ValidationError("Faltan datos para el registro")
        
        return data

    def create(self, validated_data):
        validated_data['course'] = self.context['course']
        return super(ClassroomPostSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance



class ClassroomHomeworkSerializer(serializers.ModelSerializer):
    assignment = serializers.IntegerField(source='assignment.id', required=False)
    student = serializers.CharField(source='student.id', required=False)

    class Meta:
        model = models.Homework
        fields = '__all__'

    def create(self, data):
        data['assignment'] = self.context['assignment']
        data['student'] = self.context['student']
        return super(ClassroomHomeworkSerializer, self).create(data)


class ClassroomAssignmentSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course.id', required=False)

    class Meta:
        model = models.Assignment
        fields = '__all__'

    def create(self, data):
        data['course'] = self.context['course']
        return super(ClassroomAssignmentSerializer, self).create(data)

    def validate(self, data):
        data.setdefault('title', None)
        data.setdefault('due_datetime', None)

        if None in data.values():
            raise serializers.ValidationError("Faltan datos para el registro")
        
        return data


class ClassroomCourseSerializer(serializers.ModelSerializer):
    enrolled = UserSerializer(many=True, read_only=True)
    posts = ClassroomPostSerializer(many=True, read_only=True)
    owner = serializers.CharField(source='owner.id', required=False)
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, data):
        data['owner'] = self.context['owner']
        print(data)
        #data['image'] = self.context['image']
        return super(ClassroomCourseSerializer, self).create(data)

    def validate(self, data):
        print(data.get('image'))
        data.setdefault('title', None)
        data.setdefault('day', None)
        data.setdefault('time_start', None)
        data.setdefault('time_end', None)
        data.setdefault('image', None)
        print(data.get('image'))

        if None in data.values():
            return serializers.ValidationError("Faltan datos para el registro")

        if data['day'] not in [str(i) for i in range(1, 7+1)]:
            return serializers.ValidationError("Dia fuera de rango")

        if not data['time_start'] < data['time_end']:
            return serializers.ValidationError("Horario inconsistente")

        return data