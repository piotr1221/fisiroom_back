from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views

router = SimpleRouter()
router.register(r'', views.UserViewSet, basename='users')

urlpatterns = router.urls