from rest_framework.routers import DefaultRouter
from .views import GestacionViewSet

router = DefaultRouter()
router.register(r'gestacion', GestacionViewSet, basename='gestacion')

urlpatterns = router.urls
