"""
Configuración común para las pruebas del backend SGCM (Tarea 02.04).

Antes de importar cualquier módulo de la aplicación se redirige
``DATABASE_URL`` hacia una base de datos SQLite de pruebas, separada por
completo de la base de datos de desarrollo (sgcm.db). Esto evita que las
pruebas de integración (tests/integration) escriban o borren datos reales.

También se sobreescribe la dependencia ``get_db`` de FastAPI para que cada
prueba que use el fixture ``client`` trabaje sobre esa base de datos de
pruebas, con las tablas recreadas antes de cada caso (fixture
``base_de_datos_limpia``, autouse).
"""
import os
import sys
from pathlib import Path

# Debe ejecutarse ANTES de importar app.core.database o app.main.
os.environ["DATABASE_URL"] = "sqlite:///./test_sgcm.db"

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, engine, get_db
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def base_de_datos_limpia():
    """Recrea las tablas antes de cada prueba para aislar los datos."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    """Cliente HTTP de pruebas para los controladores del API (FastAPI TestClient)."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Sesión de SQLAlchemy directa sobre la base de datos de pruebas."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def _eliminar_archivo_de_prueba():
    """Borra el archivo test_sgcm.db al finalizar toda la sesión de pruebas."""
    yield
    engine.dispose()
    archivo = ROOT_DIR / "test_sgcm.db"
    if archivo.exists():
        try:
            archivo.unlink()
        except PermissionError:
            pass
