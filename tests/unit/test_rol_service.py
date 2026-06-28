"""Pruebas unitarias de RolService (RF-C02), usando pytest + unittest.mock."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate
from app.services.rol_service import RolService


@pytest.fixture
def service():
    svc = RolService(Mock())
    svc.repo = Mock()
    return svc


def test_listar(service):
    service.repo.list.return_value = [Rol(id_rol=1, nombre_rol="Administrador")]
    resultado = service.listar()
    assert len(resultado) == 1


def test_obtener_existente(service):
    rol = Rol(id_rol=1, nombre_rol="Médico")
    service.repo.get.return_value = rol
    assert service.obtener(1) is rol


def test_obtener_inexistente(service):
    service.repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.obtener(1)
    assert exc.value.status_code == 404


def test_crear_rol_nuevo(service):
    service.repo.get_by_nombre.return_value = None
    service.repo.create.side_effect = lambda obj: obj
    data = RolCreate(nombre_rol="Contador")
    rol = service.crear(data)
    assert rol.nombre_rol == "Contador"


def test_crear_rol_duplicado(service):
    service.repo.get_by_nombre.return_value = Rol(id_rol=1, nombre_rol="Contador")
    data = RolCreate(nombre_rol="Contador")
    with pytest.raises(HTTPException) as exc:
        service.crear(data)
    assert exc.value.status_code == 400


def test_actualizar(service):
    rol = Rol(id_rol=1, nombre_rol="Contador")
    service.repo.get.return_value = rol
    service.repo.update.return_value = rol
    service.actualizar(1, RolUpdate(descripcion="Maneja ingresos y egresos"))
    service.repo.update.assert_called_once_with(rol, {"descripcion": "Maneja ingresos y egresos"})


def test_eliminar(service):
    rol = Rol(id_rol=1)
    service.repo.get.return_value = rol
    service.eliminar(1)
    service.repo.delete.assert_called_once_with(rol)
