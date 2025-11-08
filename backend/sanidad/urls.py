from rest_framework import routers
from .views import EnfermedadViewSet, MedicamentoViewSet, VacunaViewSet, RegistroSanitarioViewSet

router = routers.DefaultRouter()
router.register(r'enfermedades', EnfermedadViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'vacunas', VacunaViewSet)
router.register(r'registros', RegistroSanitarioViewSet)

urlpatterns = router.urls
