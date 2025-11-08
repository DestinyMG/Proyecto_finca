from django.db import models

class Animal(models.Model):
    TIPO_CHOICES = [
        ('Bufalo', 'Búfalo'),
        ('Vacuno', 'Vacuno'),
    ]

    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]

    ORIGEN_CHOICES = [
        ('Nacimiento', 'Nacimiento'),
        ('Compra', 'Compra'),
    ]

    # Datos generales
    codigoAnimal = models.CharField(max_length=10, unique=True)
    chip = models.CharField(max_length=30, blank=True, null=True)
    chip2 = models.CharField(max_length=30, blank=True, null=True)
    chip3 = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    procedencia = models.CharField(max_length=100)
    origen = models.CharField(max_length=10, choices=ORIGEN_CHOICES, default='Nacimiento')

    # Estado reproductivo (opcional)
    embarazada = models.BooleanField(default=False)
    fecha_palpacion = models.DateField(null=True, blank=True)
    fecha_parto = models.DateField(null=True, blank=True)

    # Campos de nacimiento (opcional)
    codigo_madre = models.CharField(max_length=10, blank=True, null=True)
    codigo_padre = models.CharField(max_length=10, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)


    # Producción de leche (solo para hembras)
    produccionLeche = models.FloatField(default=0)
    medicion = models.DateField(null=True, blank=True)
    partos = models.IntegerField(default=0)

    # Campos de compra (opcional)
    fecha_compra = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigoAnimal} ({self.tipo} - {self.sexo})"
