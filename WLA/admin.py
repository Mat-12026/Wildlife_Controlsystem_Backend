from django.contrib import admin
from .models import Tarifa, Conductor, Vehiculo, Cliente, SolicitudReserva, ReservaOperativa

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'categoria', 'pax_2', 'pax_4', 'pax_10')
    list_filter = ('categoria',)
    search_fields = ('servicio',)

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut_dni', 'telefono', 'disponibilidad', 'vencimiento_licencia')
    list_filter = ('disponibilidad',)
    search_fields = ('nombre', 'rut_dni')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'tipo_vehiculo', 'capacidad_pax', 'conductor_actual', 'fecha_revision_tecnica')
    list_filter = ('tipo_vehiculo',)
    search_fields = ('patente',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'nacionalidad', 'origen')
    search_fields = ('nombre', 'email', 'nacionalidad')
    list_filter = ('origen',)

@admin.register(SolicitudReserva)
class SolicitudReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_viaje', 'tipo_servicio', 'costo_total', 'estado_reserva')
    list_filter = ('estado_reserva', 'fecha_viaje', 'tipo_servicio')
    search_fields = ('cliente__nombre', 'punto_pickup', 'destino')

@admin.register(ReservaOperativa)
class ReservaOperativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitud', 'conductor', 'vehiculo', 'estado_pago_90')
    list_filter = ('estado_pago_90',)