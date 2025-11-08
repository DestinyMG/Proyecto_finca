from rest_framework import serializers
from .models import Gestacion

class GestacionSerializer(serializers.ModelSerializer):
    
    animal_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Gestacion
        fields = '__all__'

    def get_animal_detalle(self, obj):
        return {
            "id": obj.animal.id,
            "codigoAnimal": obj.animal.codigoAnimal,
            "tipo": obj.animal.tipo,
            "sexo": obj.animal.sexo
        }
