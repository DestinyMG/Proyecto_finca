from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.timezone import now
from .models import ProduccionLeche
from .serializers import ProduccionLecheSerializer
from animales.models import Animal
from django_filters.rest_framework import DjangoFilterBackend


class ProduccionLecheViewSet(viewsets.ModelViewSet):
    queryset = ProduccionLeche.objects.all().order_by('-fecha')
    serializer_class = ProduccionLecheSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['animal']

    # ---------------------------------------------------------------------
    # ✅ Validación: SOLO hembras pueden registrar leche
    # ---------------------------------------------------------------------
    def create(self, request, *args, **kwargs):
        animal_id = request.data.get("animal")

        if not animal_id:
            return Response({"error": "Debe seleccionar un animal"}, status=400)

        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            return Response({"error": "Animal no existe"}, status=404)

        if animal.sexo != "Hembra":
            return Response({"error": "Solo las hembras producen leche"}, status=400)

        return super().create(request, *args, **kwargs)

    # ---------------------------------------------------------------------
    # ✅ 1. Estadísticas generales de TODA la producción del hato (hembras)
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def estadisticas_generales(self, request):
        """
        Retorna:
        - total litros del año actual
        - producción por mes del año actual
        - meses con mayor y menor producción
        """

        año_actual = now().year

        # Solo hembras
        produccion = ProduccionLeche.objects.filter(
            fecha__year=año_actual,
            animal__sexo="Hembra"
        )

        # Total anual
        total_anual = produccion.aggregate(total=Sum("litros"))["total"] or 0

        # Por mes
        meses = []
        for mes in range(1, 13):
            litros_mes = produccion.filter(fecha__month=mes).aggregate(
                total=Sum("litros")
            )["total"] or 0
            meses.append({
                "mes": mes,
                "litros": litros_mes
            })

        # Buscar mayor y menor
        mayor = max(meses, key=lambda m: m["litros"])
        menor = min(meses, key=lambda m: m["litros"])

        return Response({
            "año": año_actual,
            "total_anual": total_anual,
            "produccion_mensual": meses,
            "mes_mayor_produccion": mayor,
            "mes_menor_produccion": menor
        })

    # ---------------------------------------------------------------------
    # ✅ 2. Estadísticas individuales por animal
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def estadisticas_animal(self, request):
        """
        Ejemplo:
        /api3/produccion/estadisticas_animal/?animal_id=5

        Devuelve:
        - total del año
        - litros por mes
        - mes con mayor y menor producción
        """

        animal_id = request.GET.get("animal_id")

        if not animal_id:
            return Response({"error": "Debe enviar animal_id"}, status=400)

        año_actual = now().year

        produccion = ProduccionLeche.objects.filter(
            animal_id=animal_id,
            fecha__year=año_actual
        )

        total_anual = produccion.aggregate(total=Sum("litros"))["total"] or 0

        # Por mes
        meses = []
        for mes in range(1, 13):
            litros_mes = produccion.filter(fecha__month=mes).aggregate(
                total=Sum("litros")
            )["total"] or 0
            meses.append({
                "mes": mes,
                "litros": litros_mes
            })

        mayor = max(meses, key=lambda m: m["litros"])
        menor = min(meses, key=lambda m: m["litros"])

        return Response({
            "animal_id": animal_id,
            "total_anual": total_anual,
            "produccion_mensual": meses,
            "mes_mayor_produccion": mayor,
            "mes_menor_produccion": menor
        })

    # ---------------------------------------------------------------------
    # ✅ 3. Comparar dos meses (general o por animal)
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def comparar(self, request):
        """
        Puede comparar:
        ✅ Producción general del hato (si no mandas animal_id)
        ✅ Producción de un animal específico
        Ejemplo:
        /api3/produccion/comparar/?animal_id=5&mes1=1&anio1=2025&mes2=5&anio2=2025
        """

        animal_id = request.GET.get("animal_id")
        mes1 = int(request.GET.get("mes1"))
        anio1 = int(request.GET.get("anio1"))
        mes2 = int(request.GET.get("mes2"))
        anio2 = int(request.GET.get("anio2"))

        # FILTRO BASE (general o por animal)
        filtro = {}

        if animal_id:
            filtro["animal_id"] = animal_id
        else:
            filtro["animal__sexo"] = "Hembra"

        # MES 1
        produc1 = ProduccionLeche.objects.filter(
            **filtro,
            fecha__year=anio1,
            fecha__month=mes1,
        ).aggregate(total=Sum("litros"))["total"] or 0

        # MES 2
        produc2 = ProduccionLeche.objects.filter(
            **filtro,
            fecha__year=anio2,
            fecha__month=mes2,
        ).aggregate(total=Sum("litros"))["total"] or 0

        diferencia = produc2 - produc1

        porcentaje = 0
        if produc1 > 0:
            porcentaje = round((diferencia / produc1) * 100, 2)

        return Response({
            "animal_id": animal_id,
            "mes1_total": produc1,
            "mes2_total": produc2,
            "diferencia": diferencia,
            "porcentaje": porcentaje
        })
