from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'', views.UserViewSet, basename='users')

urlpatterns = router.urls