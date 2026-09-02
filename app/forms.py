"""Formularios de la aplicación."""

from django import forms
from django.contrib.auth.models import User

from .models import Paciente, Turno


class RegistroForm(forms.Form):
    """Formulario para registrar un usuario y su paciente asociado."""

    username = forms.CharField(
        max_length=150,
        label="Usuario",
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
    )

    nombre = forms.CharField(
        max_length=100,
        label="Nombre",
    )

    apellido = forms.CharField(
        max_length=100,
        label="Apellido",
    )

    dni = forms.CharField(
        max_length=20,
        label="DNI",
    )

    email = forms.CharField(
        max_length=100,
        label="Email",
    )

    telefono = forms.CharField(
        max_length=100,
        required=False,
        label="Teléfono",
    )

    def clean_username(self):
        """Verifica que el nombre de usuario no esté registrado."""

        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "El nombre de usuario ya está registrado."
            )

        return username

    def clean_dni(self):
        """Verifica que el DNI no esté registrado."""

        dni = self.cleaned_data["dni"]

        if Paciente.objects.filter(dni=dni).exists():
            raise forms.ValidationError(
                "El DNI ya está registrado."
            )

        return dni

    def clean(self):
        """Valida los datos utilizando la validación del modelo Paciente."""

        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        dni = cleaned_data.get("dni")
        email = cleaned_data.get("email")
        usuario = None

        errors = Paciente.validate(
            nombre,
            apellido,
            dni,
            email,
            usuario,
        )

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class TurnoForm(forms.ModelForm):
    """Formulario para crear un nuevo turno."""

    class Meta:
        model = Turno
        fields = [
            "medico",
            "paciente",
            "fecha_hora",
            "motivo",
        ]
        labels = {
            "medico": "Médico",
            "paciente": "Paciente",
            "fecha_hora": "Fecha y hora",
            "motivo": "Motivo",
        }
        widgets = {
            "fecha_hora": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "motivo": forms.Textarea(
                attrs={"rows": 4}
            ),
        }