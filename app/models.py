"""Modelos de dominio de TurnoYa."""

from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Especialidad(models.Model):
    """Representa una especialidad para un medico."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        """Retorna una etiqueta legible para listados y admin."""
        return self.nombre

    def cantidad_medicos(self):
        """Retorna la cantidad de medicos que tienen una especialidad concreta."""
        return self.medico_set.count()


class Medico(models.Model):
    """Representa a un profesional médico disponible para turnos."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        """Retorna una etiqueta legible para listados y admin."""
        return f"Dr/a. {self.apellido}, {self.nombre}"

    def nombre_completo(self):
        """Retorna nombre y apellido concatenados."""
        return f"{self.nombre} {self.apellido}"

    def cantidad_turnos(self):
        """Retorna la cantidad total de turnos asociados a este médico."""
        if not hasattr(self, "turno_set"):
            return 0
        return self.turno_set.count()

    @classmethod
    def validate(cls, nombre, apellido, matricula, especialidad):
        """
        Valida los datos del médico. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio.")

        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio.")

        if not matricula or not matricula.strip():
            errors.append("La matrícula es obligatoria.")

        if not especialidad:
            errors.append("La especialidad es obligatoria.")

        return errors

    @classmethod
    def new(cls, nombre, apellido, matricula, especialidad):
        """
        Crea y persiste un nuevo médico si los datos son válidos.
        Retorna (instancia, errors). Si hay errores, instancia es None.
        """
        errors = cls.validate(nombre, apellido, matricula, especialidad)
        if errors:
            return None, errors

        medico = cls.objects.create(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            matricula=matricula.strip(),
            especialidad=especialidad
        )
        return medico, []

    def update(self, nombre, apellido, matricula, especialidad):
        """
        Actualiza los datos del médico si los datos son válidos.
        Retorna una lista de errores. Si está vacía, la actualización fue exitosa.
        """
        errors = self.__class__.validate(nombre, apellido, matricula, especialidad)
        if errors:
            return errors

        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.matricula = matricula.strip()
        self.especialidad = especialidad
        self.save()
        return []


class Paciente(models.Model):
    """Representa un paciente para un medico."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, blank=True)
    usuario = models.OneToOneField(User, related_name="paciente", on_delete=models.CASCADE)

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        """Retorna una etiqueta legible para listados y admin."""
        return f"{self.apellido}, {self.nombre}"

    def nombre_completo(self):
        """Retorna el nombre completo del paciente."""
        return f"{self.nombre} {self.apellido}"

    def cantidad_turnos(self):
        """Representa la cantidad de turnos asociados a este paciente."""
        if not hasattr(self, "turno_set"):
            return 0
        return self.turno_set.count()

    @classmethod
    def validate(cls, nombre, apellido, dni, email, usuario):
        """
        Valida los datos del paciente. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio.")

        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio.")

        if not dni or not dni.strip():
            errors.append("El dni es obligatorio.")

        if not email or not email.strip():
            errors.append("El email es obligatorio.")

        """Telefono no es obligatorio."""

        if not usuario:
            errors.append("El usuario es obligatorio.")

        return errors

    @classmethod
    def new(cls, nombre, apellido, dni, email, telefono, usuario):
        """
        Crea y persiste un nuevo paciente si los datos son válidos.
        Retorna (instancia, errors). Si hay errores, instancia es None.
        """

        errors = cls.validate(nombre, apellido, dni, email, usuario)
        if errors:
            return None, errors

        paciente = cls.objects.create(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            dni=dni.strip(),
            email=email.strip(),
            telefono=telefono.strip(),
            usuario=usuario
        )
        return paciente, []

    def update(self, nombre, apellido, dni, email, telefono, usuario):
        """
        Actualiza los datos del paciente si los datos son válidos.
        Retorna una lista de errores. Si está vacía, la actualización fue exitosa.
        """
        errors = self.__class__.validate(nombre, apellido, dni, email, usuario)
        if errors:
            return errors

        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.dni = dni.strip()
        self.email = email.strip()
        self.telefono = telefono.strip()
        self.usuario = usuario
        self.save()
        return []


class Turno(models.Model):
    """Representa un turno para un medico."""

    ESTADO_PENDIENTE = "pendiente"
    ESTADO_CONFIRMADO = "confirmado"
    ESTADO_CANCELADO = "cancelado"
    ESTADOS = [(ESTADO_PENDIENTE, "pendiente"), (ESTADO_CONFIRMADO, "confirmado"), (ESTADO_CANCELADO, "cancelado")]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    creado_por = models.ForeignKey(User, related_name="turnos", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['fecha_hora', 'estado']

    def __str__(self):
        """Retorna una etiqueta legible para listados y admin."""
        return f"{self.paciente} - {self.medico} - {self.fecha_hora}"

    def esta_pendiente(self):
        return self.estado == self.ESTADO_PENDIENTE

    def confirmar(self):
        self.estado = self.ESTADO_CONFIRMADO
        self.save()

    def cancelar(self):
        self.estado = self.ESTADO_CANCELADO
        self.save()

    @classmethod
    def validate(cls, medico, paciente, fecha_hora, motivo):
        """
        Valida los datos del turno. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        if not medico:
            errors.append("El medico es obligatorio.")

        if not paciente:
            errors.append("El paciente es obligatorio.")

        if not fecha_hora:
            errors.append("El fecha_hora es obligatorio.")

        if not motivo or not motivo.strip():
            errors.append("El motivo es obligatorio.")

        """Validacion al ingresar fechas pasadas"""
        if fecha_hora and fecha_hora < timezone.now():
            errors.append("No se pueden agendar turnos en fechas pasadas.")

        """Validacion al ingresar fechas con superposición horaria"""
        if medico and fecha_hora and cls.objects.filter(medico=medico, fecha_hora=fecha_hora).exists():
            errors.append("El medico ya tiene un turno agendado en esa fecha y hora.")

        return errors

    @classmethod
    def new(cls, medico, paciente, fecha_hora, motivo, creado_por=None):
        """
        Crea y persiste un nuevo turno si los datos son válidos.
        Retorna (instancia, errors). Si hay errores, instancia es None.
        """
        errors = cls.validate(medico, paciente, fecha_hora, motivo)
        if errors:
            return None, errors

        turno = cls.objects.create(
            medico=medico,
            paciente=paciente,
            fecha_hora=fecha_hora,
            motivo=motivo.strip(),
            creado_por=creado_por,
        )

        return turno, []

    def update(self, medico, paciente, fecha_hora, motivo):
        """
        Actualiza los datos del turno si los datos son válidos.
        Retorna una lista de errores. Si está vacía, la actualización fue exitosa.
        """
        errors = self.__class__.validate(medico, paciente, fecha_hora, motivo)
        if errors:
            return errors

        self.medico = medico
        self.paciente = paciente
        self.fecha_hora = fecha_hora
        self.motivo = motivo.strip()
        self.save()
        return []