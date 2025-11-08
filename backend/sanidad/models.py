from django.db import models
from animales.models import Animal

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Vacuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class RegistroSanitario(models.Model):
    ESTADO_CHOICES = [
        ('Sano', 'Sano'),
        ('Enfermo', 'Enfermo'),
        ('Recuperado', 'Recuperado'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='registros_sanitarios')
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Sano')
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.SET_NULL, null=True, blank=True)
    tratamiento = models.TextField(blank=True, null=True)
    medicamentos = models.ManyToManyField(Medicamento, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    # Vacunas aplicadas en esta fecha
    vacunas = models.ManyToManyField(Vacuna, blank=True)
    proxima_revision = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.animal.codigoAnimal} - {self.fecha_registro} ({self.estado})"
