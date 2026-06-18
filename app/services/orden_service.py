from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.orden_medica import OrdenMedica
from app.repositories.orden_repository import OrdenRepository
from app.repositories.consulta_repository import ConsultaRepository
from app.schemas.orden_medica import OrdenMedicaCreate


class OrdenService:
    """RF-M03: órdenes de laboratorio, imagen u otros procedimientos."""

    def __init__(self, db: Session):
        self.repo = OrdenRepository(db)
        self.consultas = ConsultaRepository(db)

    def listar_por_consulta(self, id_consulta: int):
        return self.repo.por_consulta(id_consulta)

    def crear(self, data: OrdenMedicaCreate) -> OrdenMedica:
        if not self.consultas.get(data.id_consulta):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta no encontrada")
        return self.repo.create(OrdenMedica(**data.model_dump()))
