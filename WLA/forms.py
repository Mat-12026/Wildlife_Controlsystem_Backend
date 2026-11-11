from django import forms
from .models import Tarifa, Conductor, Vehiculo, ReservaOperativa, Cliente

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['categoria', 'servicio', 'pax_2', 'pax_4', 'pax_10', 'pax_19', 'pax_24', 'pax_46']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'pax_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'pax_4': forms.NumberInput(attrs={'class': 'form-control'}),
            'pax_10': forms.NumberInput(attrs={'class': 'form-control'}),
            'pax_19': forms.NumberInput(attrs={'class': 'form-control'}),
            'pax_24': forms.NumberInput(attrs={'class': 'form-control'}),
            'pax_46': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['nombre', 'rut_dni', 'telefono', 'disponibilidad', 'vencimiento_licencia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-select'}),
            'vencimiento_licencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'tipo_vehiculo', 'capacidad_pax', 'conductor_actual', 'fecha_revision_tecnica']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'capacidad_pax': forms.NumberInput(attrs={'class': 'form-control'}),
            'conductor_actual': forms.Select(attrs={'class': 'form-select'}),
            'fecha_revision_tecnica': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AsignarReservaForm(forms.ModelForm):
    class Meta:
        model = ReservaOperativa
        fields = ['conductor', 'vehiculo', 'estado_pago_90']
        widgets = {
            'conductor': forms.Select(attrs={'class': 'form-select'}),
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'estado_pago_90': forms.Select(attrs={'class': 'form-select'}),
        }        
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'dieta', 'nacionalidad', 'edad', 'origen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dieta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Vegetariano, Sin gluten, Ninguna'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-select'}),
        }