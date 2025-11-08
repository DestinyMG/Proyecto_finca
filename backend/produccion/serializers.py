from rest_framework import serializers
from .models import ProduccionLeche

class ProduccionLecheSerializer(serializers.ModelSerializer):
    animal_codigo = serializers.ReadOnlyField(source="animal.codigoAnimal")

    class Meta:
        model = ProduccionLeche
        fields = '__all__'
