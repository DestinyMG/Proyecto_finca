from rest_framework import serializers
from .models import Enfermedad, Medicamento, Vacuna, RegistroSanitario

# Serializers simples
class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = '__all__'

# Serializer principal con detalles
class RegistroSanitarioSerializer(serializers.ModelSerializer):
    animal_codigo = serializers.ReadOnlyField(source='animal.codigoAnimal')
    enfermedad_nombre = serializers.ReadOnlyField(source='enfermedad.nombre', default=None)

    medicamentos_detalle = MedicamentoSerializer(source='medicamentos', many=True, read_only=True)
    vacunas_detalle = VacunaSerializer(source='vacunas', many=True, read_only=True)

    # ✅ PERMITIR LISTA VACÍA
    medicamentos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Medicamento.objects.all(),
        write_only=True, required=False
    )

    # ✅ ESTA ERA LA QUE TE FALLABA
    vacunas = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Vacuna.objects.all(),
        write_only=True, required=False
    )

    class Meta:
        model = RegistroSanitario
        fields = '__all__'
