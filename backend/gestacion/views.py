from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Gestacion
from .serializers import GestacionSerializer

class GestacionViewSet(viewsets.ModelViewSet):
    queryset = Gestacion.objects.all().order_by('-fecha_palpacion')
    serializer_class = GestacionSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'animal': ['exact'],
        'estado': ['exact'],
        'fecha_palpacion': ['exact', 'gte', 'lte'],
        'proxima_palpacion': ['exact', 'gte', 'lte'],
    }
