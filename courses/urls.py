from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'created', views.CourseCreatedViewSet, basename='created')
router.register(r'enrolled', views.CourseEnrolledViewSet, basename='enrolled')

urlpatterns = router.urls