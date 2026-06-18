from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.consulta_medica import ConsultaMedica
from app.models.cita import EstadoCita
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.cita_repository import CitaRepository
from app.schemas.consulta_medica import ConsultaMedicaCreate, ConsultaMedicaUpdate


class ConsultaService:
    """RF-M01: registro de anamnesis, examen físico, diagnóstico y tratamiento."""

    def __init__(self, db: Session):
        self.repo = ConsultaRepository(db)
        self.citas = CitaRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_consulta: int) -> ConsultaMedica:
        consulta = self.repo.get(id_consulta)
        if not consulta:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta no encontrada")
        return consulta

    def historial_de_paciente(self, id_paciente: int):
        """RF-P04 / RF-R02: historial clínico cronológico."""
        return self.repo.historial_por_paciente(id_paciente)

    def crear(self, data: ConsultaMedicaCreate) -> ConsultaMedica:
        cita = self.citas.get(data.id_cita)
        if not cita:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cita no encontrada")
        if cita.estado != EstadoCita.EN_ATENCION:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Solo se puede registrar una consulta para una cita EN_ATENCION",
            )
        return self.repo.create(ConsultaMedica(**data.model_dump()))

    def actualizar(self, id_consulta: int, data: ConsultaMedicaUpdate) -> ConsultaMedica:
        consulta = self.obtener(id_consulta)
        return self.repo.update(consulta, data.model_dump(exclude_unset=True))
