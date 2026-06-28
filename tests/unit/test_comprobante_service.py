"""Pruebas unitarias de ComprobanteService (RF-IE01 a RF-IE03, RF-R01, RF-R03)."""
from datetime import date
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.comprobante import Comprobante
from app.models.consulta_medica import ConsultaMedica
from app.models.cuenta_contable import CuentaContable
from app.schemas.comprobante import ComprobanteCreate
from app.services.comprobante_service import ComprobanteService


@pytest.fixture
def service():
    svc = ComprobanteService(Mock())
    svc.repo = Mock()
    svc.consultas = Mock()
    svc.cuentas = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = []
    assert service.listar() == []


def test_crear_sin_consulta(service):
    service.consultas.get.return_value = None
    data = ComprobanteCreate(id_consulta=1, tipo="factura", total=25.0, id_cuenta_contable=1)
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_sin_cuenta_contable(service):
    service.consultas.get.return_value = ConsultaMedica(id_consulta=1)
    service.cuentas.get.return_value = None
    data = ComprobanteCreate(id_consulta=1, tipo="factura", total=25.0, id_cuenta_contable=1)
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 404


def test_crear_genera_correlativo_con_estado_pendiente(service):
    service.consultas.get.return_value = ConsultaMedica(id_consulta=1)
    service.cuentas.get.return_value = CuentaContable(id_cuenta=1)
    service.repo.ultimo_correlativo.return_value = 3
    service.repo.create.side_effect = lambda obj: obj
    data = ComprobanteCreate(id_consulta=1, tipo="factura", total=25.0, id_cuenta_contable=1)
    comprobante = service.crear(data)
    assert comprobante.estado == "PENDIENTE"
    assert comprobante.numero_correlativo.endswith("000003")


def test_marcar_pagado_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.marcar_pagado(1)
    assert exc.value.status_code == 404


def test_marcar_pagado_exitoso(service):
    comprobante = Comprobante(id_comprobante=1, estado="PENDIENTE")
    service.repo.get.return_value = comprobante
    service.repo.update.return_value = comprobante
    resultado = service.marcar_pagado(1)
    service.repo.update.assert_called_once_with(comprobante, {"estado": "PAGADO"})
    assert resultado is comprobante


def test_libro_diario(service):
    service.repo.por_rango_fecha.return_value = [Comprobante(id_comprobante=1, total=10.0)]
    resultado = service.libro_diario(date(2026, 1, 1), date(2026, 1, 31))
    service.repo.por_rango_fecha.assert_called_once()
    assert len(resultado) == 1


def test_resumen_comprobantes_suma_totales(service):
    service.repo.por_rango_fecha.return_value = [
        Comprobante(id_comprobante=1, total=10.0),
        Comprobante(id_comprobante=2, total=15.5),
    ]
    resumen = service.resumen_comprobantes(date(2026, 1, 1), date(2026, 1, 31))
    assert resumen["total_periodo"] == 25.5
    assert len(resumen["comprobantes"]) == 2
