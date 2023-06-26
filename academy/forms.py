from django import forms
from .models import Temporada, Jugador, TemporadaFinalizada, Carrera

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'manager']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Nombre de la carrera',
                                             'id': 'id_nombre'}),
            'manager': forms.TextInput(attrs={'class': 'form-control mt-3',
                                             'placeholder': 'Nombre del manager',
                                             'id': 'id_manager'})
        }
        
class TemporadaForm(forms.ModelForm):
    class Meta:
        model = Temporada
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'apellido', 'nacionalidad', 'posiciones', 'edad_descubrimiento', 'media_descubrimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'posiciones': forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple', 'style':'width:200px;' , 'multiple':'mulptiple', 'name':'posiciones[]'}),
            'edad_descubrimiento': forms.NumberInput(attrs={'class': 'form-control'}),
            'media_descubrimiento': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TemporadaFinalizadaForm(forms.ModelForm):
    class Meta:
        model = TemporadaFinalizada
        fields = ['posicion_liga', 'progreso_continental', 'progreso_copa']
        widgets = {
            'posicion_liga': forms.NumberInput(attrs={'class': 'form-control'}),
            'progreso_continental': forms.Select(attrs={'class': 'form-select'}),
            'progreso_copa': forms.Select(attrs={'class': 'form-select'})
        }