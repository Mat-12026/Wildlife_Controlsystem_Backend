from rest_framework import serializers
from .models import SolicitudReserva, ReservaOperativa, Cliente, Tarifa, Vehiculo, Conductor

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class SolicitudReservaSerializer(serializers.ModelSerializer):
    cliente_detalles = ClienteSerializer(source='cliente', read_only=True)
    
    class Meta:
        model = SolicitudReserva
        fields = '__all__'

    def create(self, validated_data):
        solicitud = SolicitudReserva.objects.create(**validated_data)
        ReservaOperativa.objects.create(solicitud=solicitud, estado_pago_90='EN_ESPERA')
        return solicitud

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    conductor_nombre = serializers.CharField(source='conductor_actual.nombre', read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'

class ReservaOperativaSerializer(serializers.ModelSerializer):
    solicitud_detalles = SolicitudReservaSerializer(source='solicitud', read_only=True)
    conductor_nombre = serializers.CharField(source='conductor.nombre', read_only=True)
    vehiculo_patente = serializers.CharField(source='vehiculo.patente', read_only=True)

    class Meta:
        model = ReservaOperativa
        fields = '__all__'