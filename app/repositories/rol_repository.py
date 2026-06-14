from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.repositories.base_repository import BaseRepository


class RolRepository(BaseRepository[Rol]):
    def __init__(self, db: Session):
        super().__init__(Rol, db)

    def get_by_nombre(self, nombre: str) -> Rol | None:
        return self.db.query(Rol).filter(Rol.nombre_rol == nombre).first()
