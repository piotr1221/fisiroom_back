from decimal import Context
from os import stat
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q
from classroom.models import Assignment

from courses.models import Course
from . import serializers


class ClassroomHomeworkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomHomeworkSerializer
    queryset = serializer_class.Meta.model.objects
    http_method_names = ["post", "put"]

    def create(self, req, course_id=None, assign_id=None):  
        queryset_courses = Course.objects.filter()
        course = get_object_or_404(queryset_courses, pk=course_id)
        queryset_assigns = Assignment.objects.filter(course=course)
        assignment = get_object_or_404(queryset_assigns, pk=assign_id)

        serializer = self.serializer_class(data=req.data, context={'assignment': assignment, 'student': req.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, req, pk=None, course_id=None, assign_id=None):
        queryset = self.queryset.filter()
        homework = get_object_or_404(queryset, pk=pk, assignment=assign_id)
        homework.grade = req.data.get("grade")
        homework.save()

        serializer = self.serializer_class(homework, data = req.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomAssignmentSerializer
    queryset = serializer_class.Meta.model.objects

    def create(self, req, course_id=None):  
        queryset_courses = Course.objects.filter()
        course = get_object_or_404(queryset_courses, pk=course_id)
        serializer = self.serializer_class(data=req.data, context={'course': course})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, req, pk=None, course_id=None):
        queryset = self.queryset.filter()
        classroom_assignment = get_object_or_404(queryset, pk=pk, course=course_id)
        serializer = self.serializer_class(classroom_assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, req, pk=None, course_id=None):
        queryset = self.queryset.filter(course=course_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ClassroomCourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomCourseSerializer
    queryset = serializer_class.Meta.model.objects

    def create(self, req):
        serializer = self.serializer_class(data=req.data, context={'owner': req.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        print(serializer.data)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, req, pk=None):
        queryset = self.queryset.filter(Q(owner=req.user) | Q(id__in=req.user.enrolled_courses.all()))
        classroom_course = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(classroom_course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomPostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomPostSerializer
    queryset = serializer_class.Meta.model.objects

    def create(self, req, course_id=None):  
        queryset_courses = Course.objects.filter()
        course = get_object_or_404(queryset_courses, pk=course_id)
        serializer = self.serializer_class(data=req.data, context={'course': course})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, req, pk=None, course_id=None):
        queryset = self.queryset.filter()
        classroom_post = get_object_or_404(queryset, pk=pk, course=course_id)
        serializer = self.serializer_class(classroom_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, req, pk=None, course_id=None):
        queryset = self.queryset.filter(course=course_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, course_id=None):
        queryset = self.queryset.filter()
        classroom_post = get_object_or_404(queryset, pk=pk, course = course_id)
        serializer = self.serializer_class(classroom_post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, course_id=None):
        queryset = self.queryset.filter()
        classroom_post = get_object_or_404(queryset, pk=pk, course = course_id)
        if classroom_post:
            super().destroy(request)
            return Response({'message': 'Post borrado exitosamente'}, status = status.HTTP_200_OK)
        return Response({'message': 'No existe un post con esos datos'}, status = status.HTTP_400_BAD_REQUEST)