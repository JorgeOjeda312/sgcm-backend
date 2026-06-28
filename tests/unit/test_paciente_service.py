"""Pruebas unitarias de PacienteService (RF-P01 a RF-P03), usando pytest + unittest.mock."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate
from app.services.paciente_service import PacienteService


@pytest.fixture
def service():
    svc = PacienteService(Mock())
    svc.repo = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = [Paciente(id_paciente=1)]
    assert len(service.listar()) == 1


def test_obtener_existente(service):
    paciente = Paciente(id_paciente=1, cedula_pasaporte="0102030405")
    service.repo.get.return_value = paciente
    assert service.obtener(1) is paciente


def test_obtener_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.obtener(1)
    assert exc.value.status_code == 404


def test_buscar(service):
    service.repo.buscar.return_value = []
    resultado = service.buscar("Ojeda")
    service.repo.buscar.assert_called_once_with("Ojeda")
    assert resultado == []


def test_crear_paciente_nuevo(service):
    service.repo.get_by_cedula.return_value = None
    service.repo.create.side_effect = lambda obj: obj
    data = PacienteCreate(cedula_pasaporte="0102030405", nombre_completo="Jorge Ojeda")
    paciente = service.crear(data)
    assert paciente.cedula_pasaporte == "0102030405"


def test_crear_paciente_duplicado(service):
    service.repo.get_by_cedula.return_value = Paciente(id_paciente=1)
    data = PacienteCreate(cedula_pasaporte="0102030405", nombre_completo="Jorge Ojeda")
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 400


def test_actualizar(service):
    paciente = Paciente(id_paciente=1, nombre_completo="Jorge Ojeda")
    service.repo.get.return_value = paciente
    service.repo.update.return_value = paciente
    service.actualizar(1, PacienteUpdate(telefono="0999999999"))
    service.repo.update.assert_called_once_with(paciente, {"telefono": "0999999999"})


def test_eliminar(service):
    paciente = Paciente(id_paciente=1)
    service.repo.get.return_value = paciente
    service.eliminar(1)
    service.repo.delete.assert_called_once_with(paciente)
