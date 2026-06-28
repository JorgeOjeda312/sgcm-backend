"""Pruebas unitarias de OrdenService (RF-M03)."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.consulta_medica import ConsultaMedica
from app.models.orden_medica import OrdenMedica
from app.schemas.orden_medica import OrdenMedicaCreate
from app.services.orden_service import OrdenService


@pytest.fixture
def service():
    svc = OrdenService(Mock())
    svc.repo = Mock()
    svc.consultas = Mock()
    return svc


def test_listar_por_consulta(service):
    service.repo.por_consulta.return_value = [OrdenMedica(id_orden=1)]
    assert len(service.listar_por_consulta(1)) == 1


def test_crear_consulta_inexistente(service):
    service.consultas.get.return_value = None
    data = OrdenMedicaCreate(id_consulta=1, tipo="Laboratorio", descripcion="Biometría hemática")
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_exitosa(service):
    service.consultas.get.return_value = ConsultaMedica(id_consulta=1)
    service.repo.create.side_effect = lambda obj: obj
    data = OrdenMedicaCreate(id_consulta=1, tipo="Laboratorio", descripcion="Biometría hemática")
    orden = service.crear(data)
    assert orden.tipo == "Laboratorio"
