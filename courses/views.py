from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from . import serializers
# Create your views here.

class CourseOwnerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self, user, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.filter(owner=user).all()
        return self.serializer_class.Meta.model.objects.filter(id=pk, owner=user).first()

    def list(self, req):
        queryset = self.get_queryset(req.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, req):
        serializer = self.serializer_class(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'Curso creado con éxito'}, status=status.HTTP_201_CREATED)

class CourseStudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()