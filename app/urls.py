"""Rutas públicas de la aplicación principal."""

from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("medicos/", views.ListaMedicosView.as_view(), name="lista_medicos"),
    path("medicos/<int:pk>/", views.DetalleMedicoView.as_view(), name="detalle_medico"),
    path("turnos/nuevo/", views.NuevoTurnoView.as_view(), name="nuevo_turno"),
    # TODO:
    # path("turnos/", views.ListaTurnosView.as_view(), name="lista_turnos"),
    # path("turnos/<int:pk>/cancelar/", views.CancelarTurnoView.as_view(), name="cancelar_turno"),
]