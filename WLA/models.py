from django.db import models
from datetime import date, timedelta
from decimal import Decimal  

class Cliente(models.Model):
    ORIGEN_CHOICES = [
        ('Directo', 'Directo'),
        ('Agencia', 'Agencia'),
        ('Empresa', 'Empresa'),
    ]

    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    dieta = models.CharField(max_length=255, blank=True, null=True)
    nacionalidad = models.CharField(max_length=100)
    edad = models.IntegerField()
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES, default='Directo')
    foto_documento = models.ImageField(upload_to='documentos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.origen})"


class Tarifa(models.Model):
    CATEGORIA_CHOICES = [
        ('TRASLADO', 'Traslado'),
        ('EXCURSION', 'Excursión'),
        ('HOTEL', 'Hotel / Estancia'),
        ('CHALTEN', 'Chaltén'),
        ('CHILE', 'Chile'),
        ('OTRO', 'Otro'),
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='TRASLADO')
    servicio = models.CharField(max_length=255)
    origen = models.CharField(max_length=100, default='El Calafate')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.URLField(max_length=500, blank=True, null=True)
    
    # Precios USD por capacidad de vehículo
    pax_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pax_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pax_10 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pax_19 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pax_24 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pax_46 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.servicio} ({self.get_categoria_display()})"


class Conductor(models.Model):
    DISPONIBILIDAD_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_RUTA', 'En Ruta / En Servicio'),
        ('LICENCIA', 'De Licencia / Permiso'),
        ('NO_DISPONIBLE', 'No Disponible'),
    ]

    nombre = models.CharField(max_length=150)
    rut_dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30)
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD_CHOICES, default='DISPONIBLE')
    vencimiento_licencia = models.DateField()

    @property
    def licencia_por_vencer(self):
        return self.vencimiento_licencia <= date.today() + timedelta(days=30)

    def __str__(self):
        return f"{self.nombre} - {self.get_disponibilidad_display()}"


class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('AUTO', 'Automóvil / SUV (H/2 Pax)'),
        ('VAN', 'Van Corta (H/4 Pax)'),
        ('MINIVAN', 'Minivan (H/10 Pax)'),
        ('MINIBUS_19', 'Minibús (H/19 Pax)'),
        ('MINIBUS_24', 'Minibús (H/24 Pax)'),
        ('BUS_46', 'Manga / Bús (H/46 Pax)'),
    ]

    patente = models.CharField(max_length=20, unique=True)
    tipo_vehiculo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='VAN')
    capacidad_pax = models.IntegerField(default=4)
    conductor_actual = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiculos_asignados')
    fecha_revision_tecnica = models.DateField()

    @property
    def revision_por_vencer(self):
        return self.fecha_revision_tecnica <= date.today() + timedelta(days=30)

    def __str__(self):
        return f"{self.patente} - {self.get_tipo_vehiculo_display()}"


class SolicitudReserva(models.Model):
    ESTADO_RESERVA_CHOICES = [
        ('RESERVADO', 'Reservado (Abono 10% Realizado)'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    fecha_viaje = models.DateField()
    punto_pickup = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    cantidad_pasajeros = models.IntegerField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tipo_servicio = models.CharField(max_length=100)

    monto_abono_10 = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    saldo_pendiente_90 = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    estado_reserva = models.CharField(max_length=20, choices=ESTADO_RESERVA_CHOICES, default='RESERVADO')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.costo_total:
            monto_dec = Decimal(str(self.costo_total))
            self.monto_abono_10 = monto_dec * Decimal('0.10')
            self.saldo_pendiente_90 = monto_dec * Decimal('0.90')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre} ({self.fecha_viaje})"


class ReservaOperativa(models.Model):
    ESTADO_PAGO_90_CHOICES = [
        ('EN_ESPERA', 'En espera del Pago'),
        ('PAGADO', 'Pagado (100%)'),
    ]

    solicitud = models.OneToOneField(SolicitudReserva, on_delete=models.CASCADE, related_name='operacion')
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    estado_pago_90 = models.CharField(max_length=20, choices=ESTADO_PAGO_90_CHOICES, default='EN_ESPERA')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Operación #{self.id} - Solicitud #{self.solicitud.id}"