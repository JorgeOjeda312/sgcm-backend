from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.repositories.base_repository import BaseRepository


class PacienteRepository(BaseRepository[Paciente]):
    """RF-P02: Consulta de paciente por cédula, nombre o apellido."""

    def __init__(self, db: Session):
        super().__init__(Paciente, db)

    def get_by_cedula(self, cedula: str) -> Paciente | None:
        return self.db.query(Paciente).filter(Paciente.cedula_pasaporte == cedula).first()

    def buscar(self, texto: str, skip: int = 0, limit: int = 50) -> list[Paciente]:
        like = f"%{texto}%"
        return (
            self.db.query(Paciente)
            .filter(
                (Paciente.cedula_pasaporte.ilike(like))
                | (Paciente.nombre_completo.ilike(like))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
