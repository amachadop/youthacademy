from django.urls import path
from .views import eliminar_carrera,IndexView, CambiarEquipo, ListarJugadores, CarreraView, AgregarJugadorOjeadoView, LoginView, CrearCuentaView, cerrar_sesion, JugadorView, PasarTemporadaView,TraspasarJugador, CrearCarreraView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('carrera/<int:carrera_id>/', CarreraView.as_view(), name='carrera'),
    path('crear_carrera/', CrearCarreraView.as_view(), name='crear_carrera'),
    path('carrera/<int:carrera_id>/agregar_jugador_ojeado/', AgregarJugadorOjeadoView.as_view(), name='agregar_jugador_ojeado'),
    path('carrera/<int:carrera_id>/pasar-temporada/', PasarTemporadaView.as_view(), name='pasar_temporada'),
    path('carrera/<int:carrera_id>/cambiar-equipo/', CambiarEquipo.as_view(), name='cambiar_equipo'),
    path('jugador/<int:jugador_id>/', JugadorView.as_view(), name='jugador'),
    path('jugador/<int:jugador_id>/traspasar/<int:carrera_id>/', TraspasarJugador.as_view(), name='traspasar_jugador_ojeado'),
    path('carrera/<int:carrera_id>/jugadores/', ListarJugadores.as_view(), name='listar_jugadores'),
    path('login/', LoginView.as_view(), name='login'),
    path('crear_cuenta/', CrearCuentaView.as_view(), name='crear_cuenta'),
    path('cerrar_sesion/', cerrar_sesion, name='logout'),
    path('carrera/<int:carrera_id>/eliminar', eliminar_carrera, name='eliminar_carrera'),
]