from datetime import date, datetime, time
from sqlalchemy.orm import Session
from app.models.cita import Cita, EstadoCita
from app.repositories.base_repository import BaseRepository


class CitaRepository(BaseRepository[Cita]):
    """RF-A01, RF-A05: Calendario por médico y consulta web por cédula."""

    def __init__(self, db: Session):
        super().__init__(Cita, db)

    def disponibilidad(self, id_medico: int, fecha: date) -> list[Cita]:
        inicio = datetime.combine(fecha, time.min)
        fin = datetime.combine(fecha, time.max)
        return (
            self.db.query(Cita)
            .filter(
                Cita.id_medico == id_medico,
                Cita.fecha_hora.between(inicio, fin),
                Cita.estado != EstadoCita.CANCELADA,
            )
            .all()
        )

    def por_paciente_cedula(self, id_paciente: int) -> list[Cita]:
        return self.db.query(Cita).filter(Cita.id_paciente == id_paciente).all()
