from rest_framework import routers
from .views import ProduccionLecheViewSet

router = routers.DefaultRouter()
router.register(r'produccion', ProduccionLecheViewSet)

urlpatterns = router.urls
