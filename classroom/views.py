from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q
from . import serializers
class ClassroomCourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomCourseSerializer
    queryset = serializer_class.Meta.model.objects

    def retrieve(self, req, pk=None):
        queryset = self.queryset.filter(Q(owner=req.user) | Q(id__in=req.user.enrolled_courses.all()))
        classroom_course = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(classroom_course)
        return Response(serializer.data, status=status.HTTP_200_OK)