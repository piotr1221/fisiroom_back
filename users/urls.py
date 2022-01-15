from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path, include

main_router = SimpleRouter()
main_router.register(r'', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(main_router.urls))
]    