from django.db import models
from animales.models import Animal

class Gestacion(models.Model):
    ESTADO_CHOICES = [
        ('Gestación', 'En Gestación'),
        ('Vacía', 'Vacía'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='gestaciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    fecha_palpacion = models.DateField()

    # ✅ Ahora es opcional
    tiempo_gestacion = models.IntegerField(
        help_text="Días estimados de gestación",
        null=True,
        blank=True
    )

    proxima_palpacion = models.DateField(null=True, blank=True)

    observaciones = models.TextField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.codigoAnimal} - {self.estado}"
