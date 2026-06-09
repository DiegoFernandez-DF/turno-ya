"""Vistas iniciales para navegar médicos y pantalla de inicio."""

from django.views.generic import ListView, TemplateView, DetailView
from .models import Medico, Especialidad


class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "clinica/home.html"


class ListaMedicosView(ListView):
    """Lista todos los médicos."""

    model = Medico
    template_name = "clinica/lista_medicos.html"
    context_object_name = "medicos"

    def get_queryset(self):
        qs = Medico.objects.all()
        especialidad_id = self.request.GET.get("especialidad")
        if especialidad_id:
            qs = qs.filter(especialidad=especialidad_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["especialidades"] = Especialidad.objects.all()
        context["especialidad_seleccionada"] = self.request.GET.get("especialidad", "")
        return context


# TODO: implementar las siguientes vistas:
class DetalleMedicoView(DetailView):
    """Muestra los detalles de un medico."""

    model = Medico
    template_name = "clinica/detalle_medico.html"
    context_object_name = "medico"

# class ListaTurnosView(...): ...
# class NuevoTurnoView(...): ...
# class CancelarTurnoView(...): ...
# class ListaPacientesView(...): ...