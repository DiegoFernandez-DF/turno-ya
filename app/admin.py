"""Configuración del panel de administración de la aplicación."""

from django.contrib import admin

from .models import Especialidad, Medico, Paciente, Turno


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    """Configuración del admin para las especialidades."""

    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    """Configuración del admin para los médicos."""

    list_display = ("apellido", "nombre", "matricula", "especialidad")
    list_filter = ("especialidad",)
    search_fields = ("nombre", "apellido", "matricula")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """Configuración del admin para los pacientes."""

    list_display = ("apellido", "nombre", "dni", "email", "telefono")
    search_fields = ("nombre", "apellido", "dni", "email")


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    """Configuración del admin para los turnos."""

    list_display = (
        "fecha_hora",
        "medico",
        "paciente",
        "estado",
        "creado_por",
    )
    list_filter = ("estado", "fecha_hora")
    search_fields = (
        "medico__nombre",
        "medico__apellido",
        "paciente__nombre",
        "paciente__apellido",
    )