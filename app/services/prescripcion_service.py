from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.prescripcion import Prescripcion
from app.repositories.prescripcion_repository import PrescripcionRepository
from app.repositories.consulta_repository import ConsultaRepository
from app.schemas.prescripcion import PrescripcionCreate


class PrescripcionService:
    """RF-M02: prescripción médica con medicamento, dosis, frecuencia y duración."""

    def __init__(self, db: Session):
        self.repo = PrescripcionRepository(db)
        self.consultas = ConsultaRepository(db)

    def listar_por_consulta(self, id_consulta: int):
        return self.repo.por_consulta(id_consulta)

    def crear(self, data: PrescripcionCreate) -> Prescripcion:
        if not self.consultas.get(data.id_consulta):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta no encontrada")
        return self.repo.create(Prescripcion(**data.model_dump()))

    def marcar_impresa(self, id_prescripcion: int) -> Prescripcion:
        prescripcion = self.repo.get(id_prescripcion)
        if not prescripcion:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Prescripción no encontrada")
        return self.repo.update(prescripcion, {"impresa": True})
