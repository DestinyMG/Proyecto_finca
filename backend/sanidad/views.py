from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from rest_framework import viewsets
from .models import Enfermedad, Medicamento, Vacuna, RegistroSanitario
from .serializers import (
    EnfermedadSerializer,
    MedicamentoSerializer,
    VacunaSerializer,
    RegistroSanitarioSerializer
)


class EnfermedadViewSet(viewsets.ModelViewSet):
    queryset = Enfermedad.objects.all().order_by('nombre')
    serializer_class = EnfermedadSerializer


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all().order_by('nombre')
    serializer_class = MedicamentoSerializer


class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.all().order_by('nombre')
    serializer_class = VacunaSerializer


class RegistroSanitarioViewSet(viewsets.ModelViewSet):
    queryset = RegistroSanitario.objects.all().select_related('animal', 'enfermedad').prefetch_related('medicamentos', 'vacunas')
    serializer_class = RegistroSanitarioSerializer

    # 🔹 Habilitar filtrado
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['animal']  # <-- ahora puedes filtrar por ?animal=ID
