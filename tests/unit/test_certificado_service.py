"""Pruebas unitarias de CertificadoService (RF-CE01)."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.consulta_medica import ConsultaMedica
from app.schemas.certificado import CertificadoCreate
from app.services.certificado_service import CertificadoService


@pytest.fixture
def service():
    svc = CertificadoService(Mock())
    svc.repo = Mock()
    svc.consultas = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = []
    assert service.listar() == []


def test_crear_consulta_inexistente(service):
    service.consultas.get.return_value = None
    data = CertificadoCreate(id_consulta=1, tipo="reposo")
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_genera_correlativo(service):
    service.consultas.get.return_value = ConsultaMedica(id_consulta=1)
    service.repo.ultimo_correlativo.return_value = 7
    service.repo.create.side_effect = lambda obj: obj
    data = CertificadoCreate(id_consulta=1, tipo="reposo")
    certificado = service.crear(data)
    assert certificado.numero_correlativo.startswith("CERT-")
    assert certificado.numero_correlativo.endswith("00007")
