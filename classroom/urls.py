from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'', views.ClassroomCourseViewSet, basename='classroom')

urlpatterns = router.urls