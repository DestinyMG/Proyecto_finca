from django.db import models

# Create your models here.
from django.db import models
from animales.models import Animal
from django.core.exceptions import ValidationError

class ProduccionLeche(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='producciones')
    fecha = models.DateField()
    litros = models.FloatField()

    def clean(self):
        # Solo hembras pueden registrar leche
        if self.animal.sexo != 'Hembra':
            raise ValidationError("Solo animales hembra pueden tener producción de leche.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal.codigoAnimal} - {self.fecha} - {self.litros} litros"
