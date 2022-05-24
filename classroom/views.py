from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Q
from classroom.models import Assignment, Homework

from courses.models import Course
from . import serializers
from django.conf import settings


app_name = 'classroom'

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
        classroom_assignment = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(classroom_assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, req, pk=None, course_id=None):
        queryset = self.queryset.filter(course=course_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='homeworks')
    def homeworks(self, req, pk=None, course_id=None):
        assignment_queryset = self.queryset.filter()
        classroom_assignment = get_object_or_404(assignment_queryset, pk=pk)
        homework_queryset = classroom_assignment.homeworks
        serializer = serializers.ClassroomHomeworkSerializer(homework_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='homeworks/(?P<student_id>[^/.]+)')
    def student_homework(self, req, pk=None, course_id=None, student_id=None):
        assignment_queryset = self.queryset.filter()
        classroom_assignment = get_object_or_404(assignment_queryset, pk=pk)
        homework_queryset = classroom_assignment.homeworks
        classroom_homework = get_object_or_404(homework_queryset, student=student_id)
        serializer = serializers.ClassroomHomeworkSerializer(classroom_homework)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomCourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassroomCourseSerializer
    queryset = serializer_class.Meta.model.objects

    def create(self, req):
        serializer = self.serializer_class(data=req.data, context={'owner': req.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, req, pk=None):
        queryset = self.queryset.filter()
        classroom_course = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(classroom_course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='(?P<course_id>[^/.]+)/enroll')
    def enroll(self, req, course_id=None):
        queryset = self.queryset.filter()
        classroom_course = get_object_or_404(queryset, pk=course_id) 
        classroom_course.enrolled.add(req.user)
        try:
            classroom_course.save()
            return HttpResponseRedirect(reverse('classroom:classroom-detail', kwargs={'pk': course_id}))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class InvitationAPIView(APIView):
    http_method_names = ['get', 'post']
    ### Es necesario remover este bloque de codigo comentado para mejorar la legibilidad y la mantenibilidad
    # def get(self, request, course_id=None):
    #     subject = "Correo de Invitación"
    #     link = request.META['HTTP_HOST'] + '/classroom/' + str(course_id) + '/invitate/'
    #     # html_content = f"""
    #     # <!DOCTYPE html>
    #     # <html>
    #     # <body>

    #     # <h1>Título</h1>
    #     # <button href="{link}">Clickear</button>

    #     # </body>
    #     # </html>
    #     # """

    #     # html_content = render_to_string('./email.html', {'link': link})
    #     email_from = 'takatoguild@gmail.com',
    #     email_to = 'guilyamon_ky@hotmail.com'
    #     msg = EmailMultiAlternatives(subject, link, email_from, [email_to])
    #     # msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    #     return HttpResponseRedirect(redirect_to='https://google.com')
    
    def post(self, request, course_id):
        queryset_courses = Course.objects.filter()
        course = get_object_or_404(queryset_courses, pk=course_id)

        subject = "Correo de Invitación"
        base_link = 'https://fisiroom.netlify.app/curso/' + str(course_id) + '/unirse'
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body>

        <h1>¡Bienvenido al curso: {course.title}!</h1>
        <h2>Profesor: <h3>{course.owner.first_name} {course.owner.last_name}</h3></h2> 
        <a>Haz click</a>
        <a href="{base_link}">aquí</a>
        <a>para unirte.</a>

        </body>
        </html>
        """
        email_to = request.data['email']
        msg = EmailMultiAlternatives(subject, base_link + 'enroll/', settings.EMAIL_HOST_USER, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return Response({}, status=status.HTTP_200_OK)
