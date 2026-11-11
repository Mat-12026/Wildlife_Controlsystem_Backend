from django.urls import path
from . import views

urlpatterns = [
    # --- ENDPOINTS API REST PARA REACT ---
    path('api/servicios/', views.lista_servicios_api, name='api_lista_servicios'),
    path('api/clientes/nuevo/', views.registrar_cliente, name='api_registrar_cliente'),
    path('api/reservas/crear/', views.crear_reserva_api, name='api_crear_reserva'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/dashboard/reservas/', views.dashboard_reservas_api, name='api_dashboard_reservas'),
    path('api/dashboard/vehiculos/', views.dashboard_vehiculos_api, name='api_dashboard_vehiculos'),
    path('api/dashboard/conductores/', views.dashboard_conductores_api, name='api_dashboard_conductores'),
    path('api/dashboard/asignaciones/', views.dashboard_asignaciones_api, name='api_dashboard_asignaciones'),

    # --- INICIO / DASHBOARD ---
    path('', views.menu_principal, name='menu_principal'),
    path('menu/', views.menu_principal, name='menu_principal'),
    
    # --- MÓDULO TARIFAS ---
    path('tarifas/', views.lista_tarifas, name='lista_tarifas'),
    path('tarifas/crear/', views.crear_tarifa, name='crear_tarifa'),
    path('tarifas/editar/<int:pk>/', views.editar_tarifa, name='editar_tarifa'),
    path('tarifas/eliminar/<int:pk>/', views.eliminar_tarifa, name='eliminar_tarifa'),
    
    # --- MÓDULO CONDUCTORES ---
    path('conductores/', views.lista_conductores, name='lista_conductores'),
    path('conductores/crear/', views.crear_conductor, name='crear_conductor'),
    path('conductores/editar/<int:pk>/', views.editar_conductor, name='editar_conductor'),
    path('conductores/eliminar/<int:pk>/', views.eliminar_conductor, name='eliminar_conductor'),
    
    # --- MÓDULO FLOTA ---
    path('flota/', views.lista_flota, name='lista_flota'),
    path('flota/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('flota/editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('flota/eliminar/<int:pk>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    
    # --- MÓDULO RESERVAS ---
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/asignar/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    
    # --- MÓDULO CLIENTES ---
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
]