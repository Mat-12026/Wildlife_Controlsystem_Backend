import json
import os
import re
import urllib.error
import urllib.request
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import Tarifa, Conductor, Vehiculo, SolicitudReserva, ReservaOperativa, Cliente
from .forms import TarifaForm, ConductorForm, VehiculoForm, AsignarReservaForm, ClienteForm
from .serializers import (
    SolicitudReservaSerializer, 
    ClienteSerializer, 
    TarifaSerializer, 
    VehiculoSerializer, 
    ConductorSerializer, 
    ReservaOperativaSerializer
)


# --- 0. MENÚ PRINCIPAL (DASHBOARD NATIVO DJANGO) ---
@login_required
def menu_principal(request):
    return render(request, 'WLA/menu.html', {
        'tarifas': Tarifa.objects.all()[:3],
        'conductores': Conductor.objects.all()[:3],
        'vehiculos': Vehiculo.objects.all()[:3],
    })


# --- 1. MÓDULO TARIFAS (CRUD NATIVO) ---
@login_required
def lista_tarifas(request):
    return render(request, 'WLA/lista_tarifas.html', {'tarifas': Tarifa.objects.all()})

@login_required
@permission_required('WLA.add_tarifa', raise_exception=True)
def crear_tarifa(request):
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarifas')
    else:
        form = TarifaForm()
    return render(request, 'WLA/tarifa_form.html', {'form': form, 'accion': 'Agregar'})

@login_required
@permission_required('WLA.change_tarifa', raise_exception=True)
def editar_tarifa(request, pk):
    tarifa = get_object_or_404(Tarifa, pk=pk)
    if request.method == 'POST':
        form = TarifaForm(request.POST, instance=tarifa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarifas')
    else:
        form = TarifaForm(instance=tarifa)
    return render(request, 'WLA/tarifa_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('WLA.delete_tarifa', raise_exception=True)
def eliminar_tarifa(request, pk):
    tarifa = get_object_or_404(Tarifa, pk=pk)
    if request.method == 'POST':
        tarifa.delete()
        return redirect('lista_tarifas')
    return render(request, 'WLA/tarifa_confirm_delete.html', {'tarifa': tarifa})


# --- 2. MÓDULO CONDUCTORES (CRUD NATIVO) ---
@login_required
def lista_conductores(request):
    return render(request, 'WLA/lista_conductores.html', {'conductores': Conductor.objects.all()})

@login_required
@permission_required('WLA.add_conductor', raise_exception=True)
def crear_conductor(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_conductores')
    else:
        form = ConductorForm()
    return render(request, 'WLA/conductor_form.html', {'form': form, 'accion': 'Agregar'})

@login_required
@permission_required('WLA.change_conductor', raise_exception=True)
def editar_conductor(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)
    if request.method == 'POST':
        form = ConductorForm(request.POST, instance=conductor)
        if form.is_valid():
            form.save()
            return redirect('lista_conductores')
    else:
        form = ConductorForm(instance=conductor)
    return render(request, 'WLA/conductor_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('WLA.delete_conductor', raise_exception=True)
def eliminar_conductor(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)
    if request.method == 'POST':
        conductor.delete()
        return redirect('lista_conductores')
    return render(request, 'WLA/conductor_confirm_delete.html', {'conductor': conductor})


# --- 3. MÓDULO FLOTA / VEHÍCULOS (CRUD NATIVO) ---
@login_required
def lista_flota(request):
    return render(request, 'WLA/lista_flota.html', {'vehiculos': Vehiculo.objects.all()})

@login_required
@permission_required('WLA.add_vehiculo', raise_exception=True)
def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_flota')
    else:
        form = VehiculoForm()
    return render(request, 'WLA/vehiculo_form.html', {'form': form, 'accion': 'Agregar'})

@login_required
@permission_required('WLA.change_vehiculo', raise_exception=True)
def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('lista_flota')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'WLA/vehiculo_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('WLA.delete_vehiculo', raise_exception=True)
def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('lista_flota')
    return render(request, 'WLA/vehiculo_confirm_delete.html', {'vehiculo': vehiculo})


# --- 4. MÓDULO RESERVAS (NATIVO) ---
@login_required
def lista_reservas(request):
    reservas_operativas = ReservaOperativa.objects.select_related('solicitud', 'conductor', 'vehiculo').all()
    return render(request, 'WLA/lista_reservas.html', {'operaciones': reservas_operativas})

@login_required
def editar_operacion(request, pk):
    operacion = get_object_or_404(ReservaOperativa, pk=pk)
    if request.method == 'POST':
        form = AsignarReservaForm(request.POST, instance=operacion)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = AsignarReservaForm(instance=operacion)
    
    return render(request, 'WLA/asignar_reserva_form.html', {
        'form': form,
        'operacion': operacion
    })


# --- 5. MÓDULO CLIENTES (NATIVO) ---
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'WLA/lista_clientes.html', {'clientes': clientes})

@login_required
@permission_required('WLA.add_cliente', raise_exception=True)
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'WLA/cliente_form.html', {'form': form, 'accion': 'Agregar'})

@login_required
@permission_required('WLA.change_cliente', raise_exception=True)
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'WLA/cliente_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('WLA.delete_cliente', raise_exception=True)
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'WLA/cliente_confirm_delete.html', {'cliente': cliente})


# --- VIEWSETS CRUD COMPLETOS PARA EL DASHBOARD REACT ---

class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all().order_by('id')
    serializer_class = TarifaSerializer
    permission_classes = [AllowAny]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all().order_by('id')
    serializer_class = VehiculoSerializer
    permission_classes = [AllowAny]

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all().order_by('id')
    serializer_class = ConductorSerializer
    permission_classes = [AllowAny]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-id')
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]

class SolicitudReservaViewSet(viewsets.ModelViewSet):
    queryset = SolicitudReserva.objects.select_related('cliente').all().order_by('-created_at')
    serializer_class = SolicitudReservaSerializer
    permission_classes = [AllowAny]

class ReservaOperativaViewSet(viewsets.ModelViewSet):
    queryset = ReservaOperativa.objects.select_related('solicitud', 'conductor', 'vehiculo').all().order_by('-id')
    serializer_class = ReservaOperativaSerializer
    permission_classes = [AllowAny]


# --- API ENDPOINTS PARA REACT ---

@api_view(['GET'])
@permission_classes([AllowAny])
def consultar_patente_chile(request, patente):
    """Consulta marca, modelo y año de una patente chilena para autocompletar en flota."""
    patente_limpia = re.sub(r'[^A-Za-z0-9]', '', patente or '').upper()

    if not re.match(r'^[A-Z]{2}([A-Z]{2}|\d{2})\d{2}$', patente_limpia):
        return Response(
            {
                'encontrado': False,
                'error': 'Formato de patente chilena inválido (ej: KJHS45 o AB1234).'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    url = f'https://api.boostr.cl/vehicle/{patente_limpia}.json'
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'WildLifeAdventure/1.0'
    }
    api_key = os.environ.get('BOOSTR_API_KEY')
    if api_key:
        headers['X-API-KEY'] = api_key

    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=6) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
            data = payload.get('data') if isinstance(payload, dict) else None

            if isinstance(data, dict) and (data.get('make') or data.get('model') or data.get('year')):
                return Response({
                    'encontrado': True,
                    'patente': patente_limpia,
                    'marca': data.get('make') or '',
                    'modelo': data.get('model') or '',
                    'anio': data.get('year') or None,
                }, status=status.HTTP_200_OK)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, Exception):
        pass

    # Respaldo: verificar si la patente ya existe en PostgreSQL con datos cargados
    existente = Vehiculo.objects.filter(patente__iexact=patente_limpia).first()
    if existente and (getattr(existente, 'marca', None) or getattr(existente, 'modelo', None) or getattr(existente, 'anio', None)):
        return Response({
            'encontrado': True,
            'patente': patente_limpia,
            'marca': getattr(existente, 'marca', '') or '',
            'modelo': getattr(existente, 'modelo', '') or '',
            'anio': getattr(existente, 'anio', None),
        }, status=status.HTTP_200_OK)

    return Response({
        'encontrado': False,
        'patente': patente_limpia,
        'marca': '',
        'modelo': '',
        'anio': None,
        'mensaje': 'No se encontraron datos automáticos para esta patente. Puedes ingresar marca, modelo y año manualmente.'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def lista_servicios_api(request):
    """Retorna todas las Tarifas/Servicios para el catálogo dinámico en React."""
    tarifas = Tarifa.objects.all()
    serializer = TarifaSerializer(tarifas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def registrar_cliente(request):
    """Registra la reserva pública enviada por el cliente desde React."""
    email = request.data.get('email')
    cliente_existente = Cliente.objects.filter(email=email).first() if email else None

    if cliente_existente:
        cliente_serializer = ClienteSerializer(cliente_existente, data=request.data, partial=True)
    else:
        cliente_serializer = ClienteSerializer(data=request.data)

    if cliente_serializer.is_valid():
        cliente = cliente_serializer.save()

        datos_reserva = {
            'fecha_viaje': request.data.get('fecha_viaje'),
            'punto_pickup': request.data.get('punto_pickup'),
            'destino': request.data.get('destino'),
            'cantidad_pasajeros': request.data.get('cantidad_pasajeros'),
            'costo_total': request.data.get('costo_total'),
            'tipo_servicio': request.data.get('tipo_servicio'),
            'cliente': cliente.id
        }

        reserva_serializer = SolicitudReservaSerializer(data=datos_reserva)
        if reserva_serializer.is_valid():
            reserva_serializer.save()
            return Response({'id': cliente.id, 'mensaje': 'Cliente y Reserva procesados exitosamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error_reserva": reserva_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def crear_reserva_api(request):
    serializer = SolicitudReservaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Reserva y operación creadas con éxito', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """Valida el usuario creado en Django Admin, verifica su grupo y devuelve su ficha."""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None and user.is_active:
        es_admin = (
            user.is_superuser
            or user.groups.filter(name='Administrador').exists()
            or (user.is_staff and not user.groups.filter(name='Operador').exists())
        )
        role = 'admin' if es_admin else 'operator'
        perfil = getattr(user, 'perfil', None)
        nombre_mostrar = perfil.nombre_completo if (perfil and perfil.nombre_completo) else user.username

        return Response({
            'mensaje': 'Authentication successful',
            'username': nombre_mostrar,
            'is_staff': user.is_staff,
            'role': role
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Credenciales corporativas inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_reservas_api(request):
    reservas = SolicitudReserva.objects.select_related('cliente').all().order_by('-created_at')
    serializer = SolicitudReservaSerializer(reservas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_vehiculos_api(request):
    vehiculos = Vehiculo.objects.all()
    serializer = VehiculoSerializer(vehiculos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_conductores_api(request):
    conductores = Conductor.objects.all()
    serializer = ConductorSerializer(conductores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_asignaciones_api(request):
    asignaciones = ReservaOperativa.objects.select_related('solicitud', 'conductor', 'vehiculo').all()
    serializer = ReservaOperativaSerializer(asignaciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def notificaciones_api(request):
    """Genera alertas automáticas de vencimientos de flota/choferes, reservas y pagos."""
    hoy = date.today()
    limite_30_dias = hoy + timedelta(days=30)
    notificaciones = []

    for c in Conductor.objects.all():
        venc_lic = getattr(c, 'vencimiento_licencia', None)
        if venc_lic:
            if venc_lic < hoy:
                notificaciones.append({
                    'tipo': 'danger',
                    'categoria': 'Conductor',
                    'titulo': f'Licencia Vencida: {c.nombre}',
                    'mensaje': f'La licencia expiró el {venc_lic}.'
                })
            elif venc_lic <= limite_30_dias:
                dias = (venc_lic - hoy).days
                notificaciones.append({
                    'tipo': 'warning',
                    'categoria': 'Conductor',
                    'titulo': f'Licencia por Vencer: {c.nombre}',
                    'mensaje': f'Vence en {dias} días ({venc_lic}).'
                })

    for v in Vehiculo.objects.all():
        docs = [
            ('Revisión Técnica', getattr(v, 'fecha_revision_tecnica', None)),
            ('SOAP', getattr(v, 'fecha_soap', None)),
            ('Permiso Circulación', getattr(v, 'fecha_permiso_circulacion', None)),
        ]
        for nombre_doc, fecha_doc in docs:
            if fecha_doc:
                if fecha_doc < hoy:
                    notificaciones.append({
                        'tipo': 'danger',
                        'categoria': 'Vehículo',
                        'titulo': f'{nombre_doc} Vencido: {v.patente}',
                        'mensaje': f'Expiró el {fecha_doc}.'
                    })
                elif fecha_doc <= limite_30_dias:
                    notificaciones.append({
                        'tipo': 'warning',
                        'categoria': 'Vehículo',
                        'titulo': f'{nombre_doc} por Vencer: {v.patente}',
                        'mensaje': f'Vence el {fecha_doc}.'
                    })

    for r in SolicitudReserva.objects.select_related('cliente').all().order_by('-created_at')[:10]:
        notificaciones.append({
            'tipo': 'info',
            'categoria': 'Reserva',
            'titulo': f'Nueva Reserva #{r.id}',
            'mensaje': f'Cliente: {r.cliente.nombre} - Destino: {r.destino} ({r.fecha_viaje}).'
        })
        if hasattr(r, 'operacion'):
            if r.operacion.estado_pago_90 == 'EN_ESPERA':
                notificaciones.append({
                    'tipo': 'warning',
                    'categoria': 'Pago Pendiente',
                    'titulo': f'Cobro Pendiente (90%) - Reserva #{r.id}',
                    'mensaje': f'Saldo: ${r.saldo_pendiente_90} USD por cobrar a {r.cliente.nombre}.'
                })
            elif r.operacion.estado_pago_90 == 'PAGADO':
                notificaciones.append({
                    'tipo': 'success',
                    'categoria': 'Pago Completado',
                    'titulo': f'Pago 100% Liquidado - Reserva #{r.id}',
                    'mensaje': f'El cliente {r.cliente.nombre} completó el 100% (${r.costo_total} USD).'
                })

    return Response(notificaciones, status=status.HTTP_200_OK)