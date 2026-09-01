"""Vistas iniciales para navegar médicos y pantalla de inicio."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from .models import Medico


class HomeView(LoginRequiredMixin ,TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "clinica/home.html"


class ListaMedicosView(LoginRequiredMixin, ListView):
    """Lista todos los médicos."""

    model = Medico
    template_name = "clinica/lista_medicos.html"
    context_object_name = "medicos"

class DetalleMedicoView(LoginRequiredMixin, DetailView):
    """Muestra los detalles de un médico."""

    model = Medico
    template_name = "clinica/detalle_medico.html"
    context_object_name = "medico"

# TODO: implementar las siguientes vistas:
# class ListaTurnosView(...): ...
# class NuevoTurnoView(...): ...
# class CancelarTurnoView(...): ...
# class ListaPacientesView(...): ...