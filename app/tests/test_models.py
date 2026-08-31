"""Pruebas unitarias del modelo Medico."""
from django.contrib.auth.models import User
from django.test import TestCase
from app.models import Medico, Especialidad, Paciente, Turno
from django.utils import timezone
from datetime import timedelta


class EspecialidadModelTest(TestCase):
    """Verifica comportamiento básico y validaciones del modelo especialidad."""

    def setUp(self):
        self.especialidad = Especialidad.objects.create(
            nombre="Pediatria",
            descripcion="Atención médica para niños.",
        )

    # --- __str__ y métodos simples ---

    def test_str_retorna_nombre(self):
        self.assertEqual(str(self.especialidad), "Pediatria")

    def test_cantidad_medicos_inicial_es_cero(self):
        self.assertEqual(self.especialidad.cantidad_medicos(), 0)

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Especialidad.validate("Cardiología")
        self.assertEqual(errors, [])

    # --- new ---

    def test_new_especialidad_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Especialidad.objects.count()
        especialidad, errors = Especialidad.new("", "")
        self.assertIsNone(especialidad)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Especialidad.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        errors = self.especialidad.update("Cardiología","Atención médica especializada en cardiología.",)
        self.assertEqual(errors, [])
        self.especialidad.refresh_from_db()
        self.assertEqual(self.especialidad.nombre, "Cardiología")
        self.assertEqual(self.especialidad.descripcion, "Atención médica especializada en cardiología.",)

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.especialidad.update("", "")
        self.assertTrue(len(errors) > 0)
        self.especialidad.refresh_from_db()
        self.assertEqual(self.especialidad.nombre, "Pediatria")
        self.assertEqual(self.especialidad.descripcion, "Atención médica para niños.",)

class MedicoModelTest(TestCase):
    """Verifica comportamiento básico y validaciones del modelo medico."""

    def setUp(self):
        self.medico = Medico.objects.create(
            nombre="Laura",
            apellido="Romero",
            matricula="MP-9999",
            especialidad= Especialidad.objects.create(nombre="Pediatria"),
        )

    # --- __str__ y métodos simples ---

    def test_str_incluye_apellido_y_nombre(self):
        self.assertIn("Romero", str(self.medico))
        self.assertIn("Laura", str(self.medico))

    def test_nombre_completo(self):
        self.assertEqual(self.medico.nombre_completo(), "Laura Romero")

    def test_cantidad_turnos_inicial_es_cero(self):
        self.assertEqual(self.medico.cantidad_turnos(), 0)

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Medico.validate("Ana", "García", "MP-0001", Especialidad.objects.create(nombre="Cardiología"))
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        errors = Medico.validate("", "García", "MP-0001", Especialidad.objects.create(nombre="Cardiología"))
        self.assertTrue(len(errors) > 0)

    def test_validate_matricula_vacia_retorna_error(self):
        errors = Medico.validate("Ana", "García", "", Especialidad.objects.create(nombre="Cardiología"))
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_medico_con_datos_validos(self):
        medico, errors = Medico.new("Carlos", "López", "MP-1234", Especialidad.objects.create(nombre="Clínica Médica"))
        self.assertEqual(errors, [])
        self.assertIsNotNone(medico)
        self.assertEqual(medico.apellido, "López")
        self.assertTrue(Medico.objects.filter(matricula="MP-1234").exists())

    def test_new_medico_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Medico.objects.count()
        medico, errors = Medico.new("", "", "", "")
        self.assertIsNone(medico)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Medico.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        self.especialidad = Especialidad.objects.create(nombre="Cardiología" )
        errors = self.medico.update("Laura", "Romero", "MP-9999", self.especialidad)
        self.assertEqual(errors, [])
        self.medico.refresh_from_db()
        self.assertEqual(self.medico.especialidad, self.especialidad)

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.medico.update("", "", "", "")
        self.assertTrue(len(errors) > 0)
        self.medico.refresh_from_db()
        self.assertEqual(self.medico.nombre, "Laura")  # sin cambios

class PacienteModelTest(TestCase):
    """Verifica comportamiento básico y validaciones del modelo paciente."""

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='RodriRodriguez',
            password='1234',
        )

        self.paciente = Paciente.objects.create(
            nombre = "Rodrigo",
            apellido = "Rodriguez",
            dni = "123456789",
            email = "RRodriguez@gmail.com",
            telefono = "987654321",
            usuario = self.usuario,
        )

    # --- __str__ y métodos simples ---

    def test_str_incluye_apellido_y_nombre(self):
        self.assertIn("Rodriguez", str(self.paciente))
        self.assertIn("Rodrigo", str(self.paciente))

    def test_nombre_completo(self):
        self.assertEqual(self.paciente.nombre_completo(), "Rodrigo Rodriguez")

    def test_cantidad_turnos_inicial_es_cero(self):
        self.assertEqual(self.paciente.cantidad_turnos(), 0)

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Paciente.validate("Rodrigo", "Rodriguez", "123456789", "RRodriguez@gmail.com", self.usuario)
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        errors = Paciente.validate("", "Rodriguez", "123456789", "RRodriguez@gmail.com", self.usuario)
        self.assertTrue(len(errors) > 0)

    def test_validate_email_vacio_retorna_error(self):
        errors = Paciente.validate("Rodrigo", "Rodriguez", "123456789", "", self.usuario)
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_paciente_con_datos_validos(self):
        usuario = User.objects.create_user(
            username='JJ',
            password='1234',
        )

        paciente, errors = Paciente.new("John", "Johnson", "134679258", "JJson@gmail.com", "147852369", usuario)
        self.assertEqual(errors, [])
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.apellido, "Johnson")
        self.assertTrue(Paciente.objects.filter(dni="134679258").exists())

    def test_new_paciente_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Paciente.objects.count()
        paciente, errors = Paciente.new("", "", "", "", "", None)
        self.assertIsNone(paciente)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Paciente.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        self.nombre = "Rambo"
        errors = self.paciente.update(self.nombre, "Rodriguez", "123456789", "RRodriguez@gmail.com", "987654321", self.usuario)
        self.assertEqual(errors, [])
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.nombre, self.nombre)

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.paciente.update("", "", "", "", "", None)
        self.assertTrue(len(errors) > 0)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.nombre, "Rodrigo")  # sin cambios

class TurnoModelTest(TestCase):
    """Verifica comportamiento básico y validaciones del modelo turno."""

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='RodriRodriguez',
            password='1234',
        )

        self.especialidad = Especialidad.objects.create(
            nombre = "Pediatria"
        )

        self.medico = Medico.objects.create(
            nombre="Laura",
            apellido="Romero",
            matricula="987654321",
            especialidad=self.especialidad,
        )

        self.paciente = Paciente.objects.create(
            nombre="Rodrigo",
            apellido="Rodriguez",
            dni="123456789",
            email="RRodriguez@gmail.com",
            telefono="987654321",
            usuario=self.usuario,
        )

        self.fecha_hora = timezone.now() + timedelta(days=1)

        self.turno = Turno.objects.create(
            medico=self.medico,
            paciente=self.paciente,
            fecha_hora=self.fecha_hora,
            motivo="Consulta general",
            creado_por=self.usuario,
        )

    # --- __str__ y métodos simples ---

    def test_str_incluye_paciente_y_medico(self):
        texto = str(self.turno)
        self.assertIn("Rodriguez", texto)
        self.assertIn("Romero", texto)

    def test_esta_pendiente_inicialmente(self):
        self.assertTrue(self.turno.esta_pendiente())

    def test_confirmar_cambia_estado(self):
        self.turno.confirmar()
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, Turno.ESTADO_CONFIRMADO)

    def test_cancelar_cambia_estado(self):
        self.turno.cancelar()
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, Turno.ESTADO_CANCELADO)

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        fecha = timezone.now() + timedelta(days=2)
        errors = Turno.validate(self.medico, self.paciente, fecha, "Consulta general",)
        self.assertEqual(errors, [])

    def test_validate_medico_vacio_retorna_error(self):
        fecha = timezone.now() + timedelta(days=2)
        errors = Turno.validate(None, self.paciente, fecha, "Consulta general",)
        self.assertTrue(len(errors) > 0)

    def test_validate_paciente_vacio_retorna_error(self):
        fecha = timezone.now() + timedelta(days=2)
        errors = Turno.validate(self.medico,None, fecha, "Consulta general",)
        self.assertTrue(len(errors) > 0)

    def test_validate_fecha_vacia_retorna_error(self):
        errors = Turno.validate(self.medico, self.paciente, None, "Consulta general",)
        self.assertTrue(len(errors) > 0)

    def test_validate_motivo_vacio_retorna_error(self):
        fecha = timezone.now() + timedelta(days=2)
        errors = Turno.validate(self.medico, self.paciente, fecha, "")
        self.assertTrue(len(errors) > 0)

    def test_validate_fecha_pasada_retorna_error(self):
        fecha = timezone.now() - timedelta(days=1)
        errors = Turno.validate(self.medico, self.paciente, fecha, "Consulta general",)
        self.assertTrue(len(errors) > 0)

    def test_validate_superposicion_de_turno_retorna_error(self):
        errors = Turno.validate(self.medico, self.paciente, self.fecha_hora, "Otra consulta",)
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_turno_con_datos_validos(self):
        fecha = timezone.now() + timedelta(days=3)
        turno, errors = Turno.new(self.medico, self.paciente, fecha, "Control medico", self.usuario,)
        self.assertEqual(errors, [])
        self.assertIsNotNone(turno)
        self.assertEqual(turno.motivo, "Control medico")
        self.assertTrue(Turno.objects.filter(medico=self.medico, paciente=self.paciente, fecha_hora=fecha).exists())

    def test_new_turno_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Turno.objects.count()
        turno, errors = Turno.new(None, None, None, "", None,)
        self.assertIsNone(turno)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Turno.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        nueva_fecha = timezone.now() + timedelta(days=4)
        errors = self.turno.update(self.medico, self.paciente, nueva_fecha, "Nueva consulta",)
        self.assertEqual(errors, [])
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.fecha_hora, nueva_fecha)
        self.assertEqual(self.turno.motivo, "Nueva consulta")

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.turno.update(None, None, None, "")
        self.assertTrue(len(errors) > 0)
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.medico, self.medico)
        self.assertEqual(self.turno.paciente, self.paciente)
        self.assertEqual(self.turno.motivo, "Consulta general")