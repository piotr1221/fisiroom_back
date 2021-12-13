from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from . import serializers
# Create your views here.

class CourseCreatedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = serializer_class.Meta.model.objects

    def list(self, req):
        queryset = self.serializer_class.Meta.model.objects.filter(owner=req.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, req, pk=None):
        queryset = self.serializer_class.Meta.model.objects.filter(owner=req.user)
        course = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, req):
        serializer = self.serializer_class(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseEnrolledViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()