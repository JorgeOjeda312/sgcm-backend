from sqlalchemy.orm import Session
from app.models.orden_medica import OrdenMedica
from app.repositories.base_repository import BaseRepository


class OrdenRepository(BaseRepository[OrdenMedica]):
    def __init__(self, db: Session):
        super().__init__(OrdenMedica, db)

    def por_consulta(self, id_consulta: int) -> list[OrdenMedica]:
        return self.db.query(OrdenMedica).filter(OrdenMedica.id_consulta == id_consulta).all()
