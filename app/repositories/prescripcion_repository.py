from sqlalchemy.orm import Session
from app.models.prescripcion import Prescripcion
from app.repositories.base_repository import BaseRepository


class PrescripcionRepository(BaseRepository[Prescripcion]):
    def __init__(self, db: Session):
        super().__init__(Prescripcion, db)

    def por_consulta(self, id_consulta: int) -> list[Prescripcion]:
        return self.db.query(Prescripcion).filter(Prescripcion.id_consulta == id_consulta).all()
