from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.repositories.rol_repository import RolRepository
from app.schemas.rol import RolCreate, RolUpdate


class RolService:
    def __init__(self, db: Session):
        self.repo = RolRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_rol: int) -> Rol:
        rol = self.repo.get(id_rol)
        if not rol:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Rol no encontrado")
        return rol

    def crear(self, data: RolCreate) -> Rol:
        if self.repo.get_by_nombre(data.nombre_rol):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El rol ya existe")
        return self.repo.create(Rol(**data.model_dump()))

    def actualizar(self, id_rol: int, data: RolUpdate) -> Rol:
        rol = self.obtener(id_rol)
        return self.repo.update(rol, data.model_dump(exclude_unset=True))

    def eliminar(self, id_rol: int) -> None:
        self.repo.delete(self.obtener(id_rol))
