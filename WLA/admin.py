from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tarifa, Conductor, Vehiculo, Cliente, SolicitudReserva, ReservaOperativa, PerfilUsuario


# Crea automáticamente los grupos "Administrador" y "Operador" en Django Admin al migrar
@receiver(post_migrate)
def crear_grupos_roles(sender, **kwargs):
    if sender.label == 'WLA':
        Group.objects.get_or_create(name='Administrador')
        Group.objects.get_or_create(name='Operador')


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        campos_obligatorios = [
            'nombre_completo',
            'rut_dni',
            'fecha_nacimiento',
            'residencia',
            'telefono',
            'contacto_emergencia_nombre',
            'contacto_emergencia_telefono',
            'consentimiento_datos',
            'acepta_codigo_etica',
        ]
        for campo in campos_obligatorios:
            if campo in self.fields:
                self.fields[campo].required = True


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    form = PerfilUsuarioForm
    can_delete = False
    verbose_name_plural = 'Ficha Personal, Residencia y Cumplimiento Ético'
    fk_name = 'user'


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_nombre_completo', 'get_residencia', 'get_rol_dashboard', 'get_etica_ok', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active')

    def get_inline_instances(self, request, obj=None):
        # Muestra la ficha personal en el paso de edición tras registrar usuario y contraseña
        if obj is None:
            return []
        return [PerfilUsuarioInline(self.model, self.admin_site)]

    @admin.display(description='Nombre Completo')
    def get_nombre_completo(self, obj):
        return obj.perfil.nombre_completo if hasattr(obj, 'perfil') else 'Pendiente'

    @admin.display(description='Residencia')
    def get_residencia(self, obj):
        return obj.perfil.residencia if hasattr(obj, 'perfil') else '-'

    @admin.display(description='Rol en Dashboard')
    def get_rol_dashboard(self, obj):
        if obj.is_superuser or obj.groups.filter(name='Administrador').exists():
            return 'Administrador (CRUD Total)'
        if obj.groups.filter(name='Operador').exists():
            return 'Operador (Clientes y Reservas)'
        if obj.is_staff:
            return 'Administrador (Staff)'
        return 'Operador (Por defecto)'

    @admin.display(boolean=True, description='Ética y Datos')
    def get_etica_ok(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.consentimiento_datos and obj.perfil.acepta_codigo_etica
        return False


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