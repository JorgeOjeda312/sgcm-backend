from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.repositories.base_repository import BaseRepository


class MedicoRepository(BaseRepository[Medico]):
    """RF-CO03: Búsqueda y filtrado de colaboradores/médicos."""

    def __init__(self, db: Session):
        super().__init__(Medico, db)

    def buscar(self, texto: str | None, especialidad: str | None) -> list[Medico]:
        query = self.db.query(Medico)
        if texto:
            like = f"%{texto}%"
            query = query.filter(Medico.nombre_completo.ilike(like))
        if especialidad:
            query = query.filter(Medico.especialidad.ilike(f"%{especialidad}%"))
        return query.all()
