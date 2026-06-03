"""Pruebas unitarias del modelo Medico."""
from django.contrib.auth.models import User
from django.test import TestCase
from app.models import Medico, Especialidad, Paciente


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

    # TODO: agregar tests para Paciente y Turno cuando los implementen

class PacienteModelTest(TestCase):
    """Verifica comportamiento básico y validaciones del modelo medico."""

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

    def cantidad_turnos_inicial_es_cero(self):
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
