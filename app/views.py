"""Vistas iniciales para navegar médicos y pantalla de inicio."""

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from .models import Medico, Turno
from .forms import TurnoForm

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

class NuevoTurnoView(LoginRequiredMixin, CreateView):
    """Permite crear un nuevo turno."""

    form_class = TurnoForm
    template_name = "clinica/nuevo_turno.html"

    def form_valid(self, form):
        """Crea el turno utilizando el usuario autenticado."""

        turno, errors = Turno.new(
            medico=form.cleaned_data["medico"],
            paciente=form.cleaned_data["paciente"],
            fecha_hora=form.cleaned_data["fecha_hora"],
            motivo=form.cleaned_data["motivo"],
            creado_por=self.request.user,
        )

        if errors:
            for error in errors:
                form.add_error(None, error)
            return self.form_invalid(form)

        self.object = turno
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Indica a dónde ir después de crear el turno."""

        return "/"

# TODO: implementar las siguientes vistas:
# class ListaTurnosView(...): ...
# class CancelarTurnoView(...): ...
# class ListaPacientesView(...): ...