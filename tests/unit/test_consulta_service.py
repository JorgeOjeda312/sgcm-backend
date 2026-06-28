"""Pruebas unitarias de ConsultaService (RF-M01, RF-P04 / RF-R02)."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.cita import Cita, EstadoCita
from app.models.consulta_medica import ConsultaMedica
from app.schemas.consulta_medica import ConsultaMedicaCreate, ConsultaMedicaUpdate
from app.services.consulta_service import ConsultaService


@pytest.fixture
def service():
    svc = ConsultaService(Mock())
    svc.repo = Mock()
    svc.citas = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = []
    assert service.listar() == []


def test_obtener_existente(service):
    consulta = ConsultaMedica(id_consulta=1)
    service.repo.get.return_value = consulta
    assert service.obtener(1) is consulta


def test_obtener_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.obtener(1)
    assert exc.value.status_code == 404


def test_historial_de_paciente(service):
    service.repo.historial_por_paciente.return_value = [ConsultaMedica(id_consulta=1)]
    resultado = service.historial_de_paciente(5)
    service.repo.historial_por_paciente.assert_called_once_with(5)
    assert len(resultado) == 1


def test_crear_consulta_sin_cita_lanza_404(service):
    service.citas.get.return_value = None
    data = ConsultaMedicaCreate(id_cita=1)
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_consulta_cita_no_en_atencion_lanza_400(service):
    service.citas.get.return_value = Cita(id_cita=1, estado=EstadoCita.PENDIENTE)
    data = ConsultaMedicaCreate(id_cita=1)
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 400


def test_crear_consulta_exitosa(service):
    service.citas.get.return_value = Cita(id_cita=1, estado=EstadoCita.EN_ATENCION)
    service.repo.create.side_effect = lambda obj: obj
    data = ConsultaMedicaCreate(id_cita=1, diagnostico_cie10="J00")
    consulta = service.crear(data)
    assert consulta.diagnostico_cie10 == "J00"


def test_actualizar(service):
    consulta = ConsultaMedica(id_consulta=1)
    service.repo.get.return_value = consulta
    service.repo.update.return_value = consulta
    service.actualizar(1, ConsultaMedicaUpdate(diagnostico_cie10="J01"))
    service.repo.update.assert_called_once_with(consulta, {"diagnostico_cie10": "J01"})
