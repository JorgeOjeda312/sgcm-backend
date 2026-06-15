from sqlalchemy.orm import Session
from app.models.consulta_medica import ConsultaMedica
from app.repositories.base_repository import BaseRepository


class ConsultaRepository(BaseRepository[ConsultaMedica]):
    """RF-P04, RF-R02: Historial clínico cronológico del paciente."""

    def __init__(self, db: Session):
        super().__init__(ConsultaMedica, db)

    def historial_por_paciente(self, id_paciente: int) -> list[ConsultaMedica]:
        from app.models.cita import Cita
        return (
            self.db.query(ConsultaMedica)
            .join(Cita, Cita.id_cita == ConsultaMedica.id_cita)
            .filter(Cita.id_paciente == id_paciente)
            .order_by(ConsultaMedica.fecha_registro.asc())
            .all()
        )
