"""Pruebas unitarias de PrescripcionService (RF-M02)."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.consulta_medica import ConsultaMedica
from app.models.prescripcion import Prescripcion
from app.schemas.prescripcion import PrescripcionCreate
from app.services.prescripcion_service import PrescripcionService


@pytest.fixture
def service():
    svc = PrescripcionService(Mock())
    svc.repo = Mock()
    svc.consultas = Mock()
    return svc


def test_listar_por_consulta(service):
    service.repo.por_consulta.return_value = [Prescripcion(id_prescripcion=1)]
    resultado = service.listar_por_consulta(1)
    service.repo.por_consulta.assert_called_once_with(1)
    assert len(resultado) == 1


def test_crear_consulta_inexistente(service):
    service.consultas.get.return_value = None
    data = PrescripcionCreate(
        id_consulta=1, medicamento="Amoxicilina", dosis="500mg", frecuencia="cada 8h"
    )
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_exitosa(service):
    service.consultas.get.return_value = ConsultaMedica(id_consulta=1)
    service.repo.create.side_effect = lambda obj: obj
    data = PrescripcionCreate(
        id_consulta=1, medicamento="Amoxicilina", dosis="500mg", frecuencia="cada 8h"
    )
    prescripcion = service.crear(data)
    assert prescripcion.medicamento == "Amoxicilina"


def test_marcar_impresa_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.marcar_impresa(1)
    assert exc.value.status_code == 404


def test_marcar_impresa_exitosa(service):
    prescripcion = Prescripcion(id_prescripcion=1, impresa=False)
    service.repo.get.return_value = prescripcion
    service.repo.update.return_value = prescripcion
    service.marcar_impresa(1)
    service.repo.update.assert_called_once_with(prescripcion, {"impresa": True})
