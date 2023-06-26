from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, TemplateView, DeleteView, UpdateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Carrera, TemporadaFinalizada, Jugador, Equipo, TemporadaJugador , Temporada, TemporadaEquipo, Nacionalidad
from .forms import JugadorForm, TemporadaFinalizadaForm, CarreraForm
from .equipos import rellenar_equipos, rellenar_posiciones, rellenar_paises
from django.db.models import F, ExpressionWrapper, IntegerField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class IndexView(View):
    def get(self, request):
        rellenar_equipos()
        rellenar_posiciones()
        rellenar_paises()
        carreras = Carrera.objects.filter(usuario=request.user) if request.user.is_authenticated else []
        return render(request, 'index.html', {'carreras': carreras, 'form':CarreraForm, 'equipos':Equipo.objects.all()})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': form})

class CrearCuentaView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'crear_cuenta.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        return render(request, 'crear_cuenta.html', {'form': form})

class CrearCarreraView(LoginRequiredMixin,CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'crear_carrera.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.usuario = self.request.user
        c = form.save()
        
        temporada = Temporada(carrera=c, nombre="17/18")
        temporada.save()
        
        te = TemporadaEquipo(temporada=temporada,equipo=Equipo.objects.get(pk=request.POST['id_equipo']))
        te.save()
        
        return redirect('index')

class CarreraView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        carrera = Carrera.objects.get(pk=kwargs['carrera_id'])
        if request.user == carrera.usuario:
            return redirect('index')
        else:
            return super(CarreraView,self).dispatch(request, *args, **kwargs)
    
    def get_ultimo_equipo(self,carrera):
        equipo_actual = TemporadaEquipo.objects.filter(temporada__carrera=carrera).last().equipo
        return equipo_actual
    
    def get(self, request, carrera_id):
        carrera = Carrera.objects.get(id=carrera_id, usuario=request.user)
        
        temporadas = Temporada.objects.filter(carrera=carrera)
        temp_finalizadas = []
        equipos = []
        temp_equipos = []
        for t in temporadas:
            te = TemporadaEquipo.objects.filter(temporada=t)
            temp_equipos.append(te)
            tf = TemporadaFinalizada.objects.filter(temporada=t).first()
            temp_finalizadas.append(tf)
        for te in temp_equipos:
            for i in te:
                equipos.append(i.equipo)
        
        for e in equipos:
            while(equipos.count(e))>1:
                equipos.remove(e)
                   
        ligas = 0
        copas = 0
        continentales = 0
        while(temp_finalizadas.count(None)>0):
            temp_finalizadas.remove(None)
        total = len(temp_finalizadas)
        for tf in temp_finalizadas:
            if tf.posicion_liga == 1:
                ligas+=1
            if tf.progreso_continental == 'Campeon':
                continentales+=1
            if tf.progreso_copa == 'Campeon':
                copas+=1
        
        temporada_actual = TemporadaEquipo.objects.filter(temporada__carrera=carrera).last()
        equipo_actual = TemporadaEquipo.objects.filter(temporada=temporada_actual.temporada).last().equipo
        anio = int('20'+temporada_actual.temporada.nombre[0:2])
        jugadores_ojeados = TemporadaJugador.objects.filter(equipo=equipo_actual, temporada=temporada_actual.temporada).annotate(edad=ExpressionWrapper(anio - F('jugador__anio_nacimiento'),output_field=IntegerField()))
        return render(request, 'carrera.html', {'carrera': carrera, 'temporada_actual': temporada_actual.temporada, 'jugadores_ojeados': jugadores_ojeados,
                                                    'form':JugadorForm, 'tform': TemporadaFinalizadaForm, 'equipo_actual': equipo_actual,
                                                    'equipos':Equipo.objects.all(), 'equipos_carrera': equipos ,'equipo_final': self.get_ultimo_equipo(carrera),
                                                    'ligas': ligas, 'copas': copas, 'continentales':continentales, 'total': total})
        
class AgregarJugadorOjeadoView(LoginRequiredMixin,View):
    def post(self, request, carrera_id):
        if request.user.is_authenticated:
            carrera = Carrera.objects.get(id=carrera_id)
            form = JugadorForm(request.POST)
            if form.is_valid():
                jugador = form.save(commit=False)
                temporada_actual = TemporadaEquipo.objects.filter(temporada__carrera=carrera).last().temporada
                x = int('20'+temporada_actual.nombre[0:2])
                jugador.anio_nacimiento = x - int(jugador.edad_descubrimiento)
                jugador.save()
                
                p = jugador.posiciones
                for pos in request.POST.getlist('posiciones'):
                    p.add(pos)
                    
                equipo = TemporadaEquipo.objects.filter(temporada=temporada_actual).last().equipo
                t = TemporadaJugador(temporada=temporada_actual, equipo=equipo, jugador=jugador)
                t.save()
        
            return redirect('carrera', carrera_id=carrera_id)    
        else:
            return redirect('index')

class PasarTemporadaView(LoginRequiredMixin,View):
    
    def post(self, request, carrera_id):
        carrera = Carrera.objects.get(id=carrera_id)
        form = TemporadaFinalizadaForm(request.POST)
        if form.is_valid():
            temporada_finalizada = form.save(commit=False)
            temporada_finalizada.temporada = TemporadaEquipo.objects.filter(temporada__carrera=carrera).last().temporada 
            temporada_finalizada.save()
            
            x = int(temporada_finalizada.temporada.nombre[0:2])
            nombre = f'{x+1}/{x+2}'
            nueva_temporada = Temporada(carrera=carrera, nombre=nombre)
            nueva_temporada.save()
            
            te = TemporadaEquipo(temporada=nueva_temporada, equipo=Equipo.objects.get(pk=request.POST['id_equipo']))
            te.save()
            
            temporada_jugador = TemporadaJugador.objects.filter(temporada=temporada_finalizada.temporada)
            for tj in temporada_jugador:
                jugador = tj.jugador
                equipo = tj.equipo
                if tj == TemporadaJugador.objects.filter(temporada=tj.temporada,jugador=jugador).last():
                    nt = TemporadaJugador(temporada=nueva_temporada,jugador=jugador,equipo=equipo)
                    nt.save()
            
        return redirect('carrera', carrera_id=carrera.id)
    
class CambiarEquipo(LoginRequiredMixin,View):
    def post(self, request, carrera_id):
        carrera = Carrera.objects.get(id=carrera_id)
        
        te = TemporadaEquipo(temporada=Temporada.objects.filter(carrera=carrera).last(), equipo=Equipo.objects.get(pk=request.POST['id_equipo']))
        te.save()
            
        return redirect('carrera', carrera_id=carrera.id)

class JugadorView(LoginRequiredMixin,View):
    def get(self, request, jugador_id):
        if request.user.is_authenticated:
            jugador = Jugador.objects.filter(id=jugador_id)
            equipos_temporadas = TemporadaJugador.objects.filter(jugador=jugador.last())
            anio = int('20'+equipos_temporadas.last().temporada.nombre[0:2])
            jugador = jugador.annotate(edad=ExpressionWrapper(anio - F('anio_nacimiento'),output_field=IntegerField())).last()
            return render(request, 'jugador.html', {'jugador': jugador, 'equipos_temporadas': equipos_temporadas, 'equipos':Equipo.objects.all(),
                                                    'carrera':equipos_temporadas.first().temporada.carrera})
        else:
            return redirect('index')

class TraspasarJugador(LoginRequiredMixin,View):
    def post(self, request, jugador_id, carrera_id):
        jugador = Jugador.objects.get(pk=jugador_id)
        equipo = Equipo.objects.get(pk=request.POST['id_equipo'])
        temporada = Temporada.objects.filter(carrera=Carrera.objects.get(pk=carrera_id)).last()
        
        te = TemporadaJugador(jugador=jugador, equipo=equipo, temporada=temporada)
        te.save()
        
        return redirect('jugador', jugador_id=jugador_id)

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

class ListarJugadores(LoginRequiredMixin,TemplateView):
    template_name = 'lista_jugadores.html'
    
    def dispatch(self, request, *args, **kwargs):
        carrera = Carrera.objects.get(pk=kwargs['carrera_id'])
        if request.user == carrera.usuario:
            return redirect('index')
        else:
            return super(ListarJugadores,self).dispatch(request, *args, **kwargs)
    
    def get(self, request, carrera_id):
        temporada = Temporada.objects.filter(carrera=Carrera.objects.get(pk=carrera_id)).last()
        anio = int('20'+temporada.nombre[0:2])
        tj = TemporadaJugador.objects.filter(temporada=temporada).annotate(edad=ExpressionWrapper(anio - F('jugador__anio_nacimiento'),output_field=IntegerField()))
        for i in tj:
            if i != tj.filter(jugador=i.jugador).last():
                tj = tj.exclude(jugador=i.jugador, equipo=i.equipo)
        
        return render(request, self.template_name, {
            'jugadores':tj,
            'carrera': Carrera.objects.get(pk=carrera_id),
            'nacionalidad': Nacionalidad.objects.all()
        })
        
    def post(self, request, carrera_id):
        temporada = Temporada.objects.filter(carrera=Carrera.objects.get(pk=carrera_id)).last()
        anio = int('20'+temporada.nombre[0:2])
        tj = TemporadaJugador.objects.filter(temporada=temporada, jugador__nombre__contains=request.POST['keywords']).annotate(edad=ExpressionWrapper(anio - F('jugador__anio_nacimiento'),output_field=IntegerField()))
        if len(list(tj.values())) == 0:
            tj = TemporadaJugador.objects.filter(temporada=temporada, jugador__apellido__contains=request.POST['keywords']).annotate(edad=ExpressionWrapper(anio - F('jugador__anio_nacimiento'),output_field=IntegerField()))
        for i in tj:
            if i != tj.filter(jugador=i.jugador).last():
                tj = tj.exclude(jugador=i.jugador, equipo=i.equipo)
        if request.POST['nacionalidad'] != '':
            tj = tj.filter(jugador__nacionalidad__pk=request.POST['nacionalidad'])
        return render(request, self.template_name, {
            'jugadores':tj,
            'carrera': Carrera.objects.get(pk=carrera_id),
            'nacionalidad': Nacionalidad.objects.all()
        })
    
@login_required    
def eliminar_carrera(request, carrera_id):
    carrera = Carrera.objects.get(pk=carrera_id)
    if carrera.usuario == request.user:
        carrera.delete()
    return redirect('index')