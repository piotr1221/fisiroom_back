from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path, include

main_router = SimpleRouter()
main_router.register(r'', views.UserViewSet, basename='users')

grade_router = SimpleRouter()
grade_router.register(r'', views.UserGradeViewSet, basename='grades')

urlpatterns = [
    path('', include(main_router.urls)),
    path('grades/', include(grade_router.urls))   
]    