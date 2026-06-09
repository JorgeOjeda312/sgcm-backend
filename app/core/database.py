"""
Configuración de la base de datos.

Se utiliza SQLAlchemy con SQLite por defecto para facilitar la ejecución
local y la evaluación del proyecto sin depender de un servidor externo.
Para un entorno de producción basta con cambiar la variable de entorno
DATABASE_URL (por ejemplo a PostgreSQL, tal como se definió en la SRS).
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sgcm.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesión de base de datos por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
