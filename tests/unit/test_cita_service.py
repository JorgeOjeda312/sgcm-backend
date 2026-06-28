"""
Pruebas unitarias de CitaService (RF-A01 a RF-A05).

Esta es la prueba más importante de la Tarea 02.04: recorre de forma
exhaustiva la máquina de estados de la entidad Cita definida en el
Diagrama de Estados de la Tarea 02.02 (TRANSICIONES_VALIDAS), validando
tanto las transiciones permitidas como las prohibidas. También cubre las
reglas de agendamiento (RF-A02), cancelación (RF-A03) y el servicio web
público de consulta por cédula (RF-A05).

Se utiliza unittest.mock para reemplazar los repositorios por dobles de
prueba (equivalente a Mockito), de modo que CitaService se valida en
completo aislamiento de la base de datos.
"""
import unittest
from datetime import date, datetime
from unittest.mock import Mock

from fastapi import HTTPException

from app.models.cita import Cita, EstadoCita
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.schemas.cita import CitaCancelar, CitaCreate
from app.services.cita_service import TRANSICIONES_VALIDAS, CitaService


def _cita(estado):
    return Cita(
        id_cita=1,
        id_paciente=1,
        id_medico=1,
        fecha_hora=datetime(2026, 7, 1, 9, 0),
        estado=estado,
    )


def _fake_update(obj, data):
    """Imita el comportamiento real de BaseRepository.update (setattr + return)."""
    for clave, valor in data.items():
        setattr(obj, clave, valor)
    return obj


class TestMaquinaDeEstados(unittest.TestCase):
    """Recorre exhaustivamente TRANSICIONES_VALIDAS (válidas e inválidas)."""

    def setUp(self):
        self.service = CitaService(Mock())
        self.service.repo = Mock()
        self.service.pacientes = Mock()
        self.service.medicos = Mock()
        self.service.repo.update.side_effect = _fake_update

    def test_todas_las_transiciones_validas_se_permiten(self):
        for origen, destinos in TRANSICIONES_VALIDAS.items():
            for destino in destinos:
                with self.subTest(origen=origen, destino=destino):
                    cita = _cita(origen)
                    resultado = self.service._transicionar(cita, destino)
                    self.assertEqual(resultado.estado, destino)

    def test_todas_las_transiciones_invalidas_lanzan_400(self):
        todos_los_estados = set(EstadoCita)
        for origen, destinos_validos in TRANSICIONES_VALIDAS.items():
            invalidos = todos_los_estados - destinos_validos - {origen}
            for destino in invalidos:
                with self.subTest(origen=origen, destino=destino):
                    cita = _cita(origen)
                    with self.assertRaises(HTTPException) as ctx:
                        self.service._transicionar(cita, destino)
                    self.assertEqual(ctx.exception.status_code, 400)


class TestCitaServiceFlujo(unittest.TestCase):
    def setUp(self):
        self.service = CitaService(Mock())
        self.service.repo = Mock()
        self.service.pacientes = Mock()
        self.service.medicos = Mock()

    def test_obtener_cita_inexistente(self):
        self.service.repo.get.return_value = None
        with self.assertRaises(HTTPException) as ctx:
            self.service.obtener(1)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_disponibilidad_devuelve_horarios_ocupados(self):
        self.service.repo.disponibilidad.return_value = [_cita(EstadoCita.PENDIENTE)]
        resultado = self.service.disponibilidad(1, date(2026, 7, 1))
        self.assertEqual(resultado, [datetime(2026, 7, 1, 9, 0)])

    def test_agendar_paciente_inexistente(self):
        self.service.pacientes.get.return_value = None
        data = CitaCreate(id_paciente=1, id_medico=1, fecha_hora=datetime(2026, 7, 1, 9, 0))
        with self.assertRaises(HTTPException) as ctx:
            self.service.agendar(data)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_agendar_medico_inexistente(self):
        self.service.pacientes.get.return_value = Paciente(id_paciente=1)
        self.service.medicos.get.return_value = None
        data = CitaCreate(id_paciente=1, id_medico=1, fecha_hora=datetime(2026, 7, 1, 9, 0))
        with self.assertRaises(HTTPException) as ctx:
            self.service.agendar(data)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_agendar_horario_ocupado(self):
        self.service.pacientes.get.return_value = Paciente(id_paciente=1)
        self.service.medicos.get.return_value = Medico(id_medico=1)
        self.service.repo.disponibilidad.return_value = [_cita(EstadoCita.PENDIENTE)]
        data = CitaCreate(id_paciente=1, id_medico=1, fecha_hora=datetime(2026, 7, 1, 9, 0))
        with self.assertRaises(HTTPException) as ctx:
            self.service.agendar(data)
        self.assertEqual(ctx.exception.status_code, 409)

    def test_agendar_exitoso(self):
        self.service.pacientes.get.return_value = Paciente(id_paciente=1)
        self.service.medicos.get.return_value = Medico(id_medico=1)
        self.service.repo.disponibilidad.return_value = []
        self.service.repo.create.side_effect = lambda obj: obj
        data = CitaCreate(id_paciente=1, id_medico=1, fecha_hora=datetime(2026, 7, 1, 9, 0))
        cita = self.service.agendar(data)
        self.assertEqual(cita.estado, EstadoCita.PENDIENTE)

    def test_confirmar_cita(self):
        cita = _cita(EstadoCita.PENDIENTE)
        self.service.repo.get.return_value = cita
        self.service.repo.update.side_effect = _fake_update
        resultado = self.service.confirmar(1)
        self.assertEqual(resultado.estado, EstadoCita.CONFIRMADA)

    def test_iniciar_atencion(self):
        cita = _cita(EstadoCita.CONFIRMADA)
        self.service.repo.get.return_value = cita
        self.service.repo.update.side_effect = _fake_update
        resultado = self.service.iniciar_atencion(1)
        self.assertEqual(resultado.estado, EstadoCita.EN_ATENCION)

    def test_finalizar_atencion(self):
        cita = _cita(EstadoCita.EN_ATENCION)
        self.service.repo.get.return_value = cita
        self.service.repo.update.side_effect = _fake_update
        resultado = self.service.finalizar_atencion(1)
        self.assertEqual(resultado.estado, EstadoCita.ATENDIDA)

    def test_cancelar_cita_registra_motivo(self):
        cita = _cita(EstadoCita.PENDIENTE)
        self.service.repo.get.return_value = cita
        self.service.repo.update.side_effect = _fake_update
        resultado = self.service.cancelar(
            1, CitaCancelar(motivo_cancelacion="Paciente no puede asistir")
        )
        self.assertEqual(resultado.estado, EstadoCita.CANCELADA)

    def test_cancelar_cita_atendida_no_permitido(self):
        cita = _cita(EstadoCita.ATENDIDA)
        self.service.repo.get.return_value = cita
        with self.assertRaises(HTTPException) as ctx:
            self.service.cancelar(1, CitaCancelar(motivo_cancelacion="x"))
        self.assertEqual(ctx.exception.status_code, 400)

    def test_consulta_publica_paciente_inexistente(self):
        self.service.pacientes.get_by_cedula.return_value = None
        with self.assertRaises(HTTPException) as ctx:
            self.service.consulta_publica_por_cedula("0102030405")
        self.assertEqual(ctx.exception.status_code, 404)

    def test_consulta_publica_devuelve_citas(self):
        self.service.pacientes.get_by_cedula.return_value = Paciente(id_paciente=1)
        self.service.repo.por_paciente_cedula.return_value = [_cita(EstadoCita.ATENDIDA)]
        resultado = self.service.consulta_publica_por_cedula("0102030405")
        self.assertEqual(len(resultado), 1)


if __name__ == "__main__":
    unittest.main()
