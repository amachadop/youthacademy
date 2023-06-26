from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Carrera)
admin.site.register(Temporada)
admin.site.register(Equipo)
admin.site.register(TemporadaEquipo)
admin.site.register(Jugador)
admin.site.register(Posicion)
admin.site.register(TemporadaJugador)
admin.site.register(TemporadaFinalizada)
admin.site.register(Nacionalidad)