from django.urls import path, include

from rest_framework.routers import SimpleRouter
from . import views

main_router = SimpleRouter()
main_router.register(r'', views.ClassroomCourseViewSet, basename='classroom')

post_router = SimpleRouter()
post_router.register(r'posts', views.ClassroomPostViewSet, basename='posts')

assignment_router = SimpleRouter()
assignment_router.register(r'assignments', views.ClassroomAssignmentViewSet, basename='assignments')

homework_router = SimpleRouter()
homework_router.register(r'submit', views.ClassroomHomeworkViewSet, basename='homework')

urlpatterns = [
    path('', include(main_router.urls)),
    path('<int:course_id>/', include(post_router.urls)),
    path('<int:course_id>/', include(assignment_router.urls)),
    path('<int:course_id>/assignments/<int:assign_id>/', include(homework_router.urls))
]       