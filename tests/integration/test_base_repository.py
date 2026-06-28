"""
Pruebas de integración de BaseRepository (patrón Repository genérico).

Se utiliza RolRepository como implementación concreta para ejercitar los
métodos genéricos get, list, create, update y delete contra una base de
datos SQLite en memoria, completamente aislada de la base de datos de
desarrollo y de la base de datos de pruebas del API (tests/conftest.py).
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.rol import Rol
from app.repositories.rol_repository import RolRepository


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    sesion = sessionmaker(bind=engine)()
    try:
        yield sesion
    finally:
        sesion.close()


@pytest.fixture
def repo(db):
    return RolRepository(db)


def test_create_y_get(repo):
    creado = repo.create(Rol(nombre_rol="Administrador"))
    assert creado.id_rol is not None
    encontrado = repo.get(creado.id_rol)
    assert encontrado.nombre_rol == "Administrador"


def test_get_inexistente_devuelve_none(repo):
    assert repo.get(999) is None


def test_list_devuelve_todos(repo):
    repo.create(Rol(nombre_rol="Administrador"))
    repo.create(Rol(nombre_rol="Médico"))
    assert len(repo.list()) == 2


def test_list_respeta_skip_y_limit(repo):
    for i in range(5):
        repo.create(Rol(nombre_rol=f"Rol-{i}"))
    pagina = repo.list(skip=2, limit=2)
    assert len(pagina) == 2


def test_update_modifica_campos(repo):
    rol = repo.create(Rol(nombre_rol="Recepcionista"))
    actualizado = repo.update(rol, {"descripcion": "Gestiona agenda de citas"})
    assert actualizado.descripcion == "Gestiona agenda de citas"


def test_delete_elimina_el_registro(repo):
    rol = repo.create(Rol(nombre_rol="Temporal"))
    repo.delete(rol)
    assert repo.get(rol.id_rol) is None


def test_get_by_nombre_de_rol_repository(repo):
    repo.create(Rol(nombre_rol="Contador"))
    assert repo.get_by_nombre("Contador") is not None
    assert repo.get_by_nombre("Inexistente") is None
