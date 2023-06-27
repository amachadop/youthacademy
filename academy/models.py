from django.db import models
from django.contrib.auth.models import User

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    manager = models.CharField(max_length=75)

class Temporada(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

class Equipo(models.Model):
    nombre = models.CharField(max_length=255)
    liga = models.CharField(max_length=255)
    
class TemporadaEquipo(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    
class Nacionalidad(models.Model):
    pais = models.CharField(max_length=80)
    bandera = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.pais}'

class Jugador(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    anio_nacimiento = models.PositiveIntegerField()
    edad_descubrimiento = models.PositiveIntegerField()
    media_descubrimiento = models.PositiveIntegerField()
    valor_inicial = models.PositiveIntegerField()
    
class JugadorPosicion(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    posicion = models.CharField(max_length=3, choices=(
        ('POR', 'Portero'),
        ('LD', 'Lateral Derecho'),
        ('LI', 'Lateral Izquierdo'),
        ('DFC', 'Defensa Central'),
        ('MCD', 'Mediocampista Defensivo'),
        ('MC', 'Mediocampista Central'),
        ('MI', 'Mediocampista Izquierdo'),
        ('MD', 'Mediocampista Derecho'),
        ('MCO', 'Mediocampista Ofensivo'),
        ('SD', 'Segundo Delantero'),
        ('EI', 'Extremo Izquierdo'),
        ('ED', 'Extremo Derecho'),
        ('DC', 'Delantero Centro'),))

class TemporadaJugador(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    media = models.PositiveIntegerField()

class TemporadaFinalizada(models.Model):
    TEMPORADA_POSICION_CHOICES = [(i, str(i)) for i in range(1, 23)]
    PROGRESO_CHOICES = (
        ('No clasificado', 'No clasificado'),
        ('Ronda 1', 'Ronda 1'),
        ('Ronda 2', 'Ronda 2'),
        ('Ronda 3', 'Ronda 3'),
        ('16º', '16º'),
        ('8º', '8º'),
        ('4º', '4º'),
        ('Semifinales', 'Semifinales'),
        ('Final', 'Final'),
        ('Campeon', 'Campeon'),
    )

    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    posicion_liga = models.PositiveIntegerField(choices=TEMPORADA_POSICION_CHOICES)
    progreso_continental = models.CharField(max_length=255, choices=PROGRESO_CHOICES)
    progreso_copa = models.CharField(max_length=255, choices=PROGRESO_CHOICES)
