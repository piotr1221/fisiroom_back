from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'owner', views.CourseOwnerViewSet, basename='courses_owner')
router.register(r'student', views.CourseStudentViewSet, basename='courses_student')

urlpatterns = router.urls