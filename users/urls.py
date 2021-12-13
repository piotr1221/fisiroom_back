from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')

urlpatterns = router.urls
urlpatterns += [
    path('login/', views.login),
]
