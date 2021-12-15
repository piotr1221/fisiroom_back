from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, redirect
from . import serializers
# Create your views here.

class CourseCreatedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseCardSerializer
    queryset = serializer_class.Meta.model.objects

    def list(self, req):
        queryset = self.queryset.filter(owner=req.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, req, pk=None):
        queryset = self.queryset.filter(owner=req.user)
        course = get_object_or_404(queryset, pk=pk)
        return redirect(course)

    def create(self, req):
        serializer = self.serializer_class(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseEnrolledViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseCardSerializer
    queryset = serializer_class.Meta.model.objects

    def list(self, req):
        queryset = self.queryset.filter(enrolled=req.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, req, pk=None):
        queryset = self.queryset.filter(enrolled=req.user)
        course = get_object_or_404(queryset, pk=pk)
        return redirect(course)