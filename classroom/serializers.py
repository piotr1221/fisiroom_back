from rest_framework import serializers
from courses.models import Course
from courses.serializers import CourseCardSerializer
from users.serializers import UserSerializer
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

    class Meta:
        model = Course
        fields = '__all__'


