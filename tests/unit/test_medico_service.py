"""Pruebas unitarias de MedicoService (RF-CO01 a RF-CO03), usando pytest + unittest.mock."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.medico import Medico
from app.schemas.medico import MedicoCreate, MedicoUpdate
from app.services.medico_service import MedicoService


@pytest.fixture
def service():
    svc = MedicoService(Mock())
    svc.repo = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = [Medico(id_medico=1)]
    assert len(service.listar()) == 1


def test_obtener_existente(service):
    medico = Medico(id_medico=1)
    service.repo.get.return_value = medico
    assert service.obtener(1) is medico


def test_obtener_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.obtener(1)
    assert exc.value.status_code == 404


def test_buscar(service):
    service.repo.buscar.return_value = []
    service.buscar("Pérez", "Pediatría")
    service.repo.buscar.assert_called_once_with("Pérez", "Pediatría")


def test_crear(service):
    service.repo.create.side_effect = lambda obj: obj
    data = MedicoCreate(
        nombre_completo="Dra. Pérez", especialidad="Pediatría", registro_senescyt="SEN-001"
    )
    medico = service.crear(data)
    assert medico.especialidad == "Pediatría"


def test_actualizar(service):
    medico = Medico(id_medico=1, especialidad="Pediatría")
    service.repo.get.return_value = medico
    service.repo.update.return_value = medico
    service.actualizar(1, MedicoUpdate(consultorio_asignado="Consultorio 3"))
    service.repo.update.assert_called_once_with(medico, {"consultorio_asignado": "Consultorio 3"})


def test_eliminar(service):
    medico = Medico(id_medico=1)
    service.repo.get.return_value = medico
    service.eliminar(1)
    service.repo.delete.assert_called_once_with(medico)
