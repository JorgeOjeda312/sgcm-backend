"""
Repositorio base genérico (patrón Repository).

Encapsula el acceso a datos mediante SQLAlchemy para que la capa de
servicio nunca interactúe directamente con la sesión de base de datos.
Cada repositorio concreto extiende esta clase y agrega consultas propias
del dominio (por ejemplo, búsqueda por cédula o por disponibilidad).
"""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id_: int) -> Optional[ModelType]:
        return self.db.get(self.model, id_)

    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType, data: dict) -> ModelType:
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()
