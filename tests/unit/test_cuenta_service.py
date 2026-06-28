"""Pruebas unitarias de CuentaService (RF-C04)."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.cuenta_contable import CuentaContable
from app.schemas.cuenta_contable import CuentaContableCreate
from app.services.cuenta_service import CuentaService


@pytest.fixture
def service():
    svc = CuentaService(Mock())
    svc.repo = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = []
    assert service.listar() == []


def test_crear_codigo_duplicado(service):
    service.repo.get_by_codigo.return_value = CuentaContable(id_cuenta=1, codigo="4101")
    data = CuentaContableCreate(codigo="4101", nombre_cuenta="Consultas médicas", tipo="INGRESO")
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 400


def test_crear_exitosa(service):
    service.repo.get_by_codigo.return_value = None
    service.repo.create.side_effect = lambda obj: obj
    data = CuentaContableCreate(codigo="4101", nombre_cuenta="Consultas médicas", tipo="INGRESO")
    cuenta = service.crear(data)
    assert cuenta.codigo == "4101"
