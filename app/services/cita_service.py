from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.cita import Cita, EstadoCita
from app.repositories.cita_repository import CitaRepository
from app.repositories.paciente_repository import PacienteRepository
from app.repositories.medico_repository import MedicoRepository
from app.schemas.cita import CitaCreate, CitaCancelar

# Transiciones válidas del Diagrama de Estados (Tarea 02.02 - IEEE 1016)
TRANSICIONES_VALIDAS = {
    EstadoCita.PENDIENTE: {EstadoCita.CONFIRMADA, EstadoCita.CANCELADA},
    EstadoCita.CONFIRMADA: {EstadoCita.EN_ATENCION, EstadoCita.CANCELADA, EstadoCita.NO_PRESENTADA},
    EstadoCita.EN_ATENCION: {EstadoCita.ATENDIDA},
    EstadoCita.ATENDIDA: set(),
    EstadoCita.CANCELADA: set(),
    EstadoCita.NO_PRESENTADA: set(),
}


class CitaService:
    """RF-A01 a RF-A05: agenda, reserva, cancelación y consulta web de citas."""

    def __init__(self, db: Session):
        self.repo = CitaRepository(db)
        self.pacientes = PacienteRepository(db)
        self.medicos = MedicoRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_cita: int) -> Cita:
        cita = self.repo.get(id_cita)
        if not cita:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cita no encontrada")
        return cita

    def disponibilidad(self, id_medico: int, fecha: date):
        """RF-A01: slots ocupados de un médico para una fecha determinada."""
        ocupadas = self.repo.disponibilidad(id_medico, fecha)
        return [c.fecha_hora for c in ocupadas]

    def agendar(self, data: CitaCreate) -> Cita:
        """RF-A02: valida paciente, médico y choque de horario antes de reservar."""
        if not self.pacientes.get(data.id_paciente):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Paciente no encontrado")
        if not self.medicos.get(data.id_medico):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Médico no encontrado")

        ocupadas = self.repo.disponibilidad(data.id_medico, data.fecha_hora.date())
        if any(c.fecha_hora == data.fecha_hora for c in ocupadas):
            raise HTTPException(status.HTTP_409_CONFLICT, "El horario ya está ocupado")

        cita = Cita(**data.model_dump(), estado=EstadoCita.PENDIENTE)
        return self.repo.create(cita)

    def _transicionar(self, cita: Cita, nuevo_estado: EstadoCita) -> Cita:
        if nuevo_estado not in TRANSICIONES_VALIDAS[cita.estado]:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Transición inválida: {cita.estado.value} -> {nuevo_estado.value}",
            )
        return self.repo.update(cita, {"estado": nuevo_estado})

    def confirmar(self, id_cita: int) -> Cita:
        cita = self.obtener(id_cita)
        return self._transicionar(cita, EstadoCita.CONFIRMADA)

    def iniciar_atencion(self, id_cita: int) -> Cita:
        cita = self.obtener(id_cita)
        return self._transicionar(cita, EstadoCita.EN_ATENCION)

    def finalizar_atencion(self, id_cita: int) -> Cita:
        cita = self.obtener(id_cita)
        return self._transicionar(cita, EstadoCita.ATENDIDA)

    def cancelar(self, id_cita: int, data: CitaCancelar) -> Cita:
        """RF-A03: cancela la cita y libera el slot automáticamente."""
        cita = self.obtener(id_cita)
        cita = self._transicionar(cita, EstadoCita.CANCELADA)
        return self.repo.update(cita, {"motivo_cancelacion": data.motivo_cancelacion})

    def consulta_publica_por_cedula(self, cedula: str):
        """RF-A05: servicio web público que retorna citas por cédula del paciente."""
        paciente = self.pacientes.get_by_cedula(cedula)
        if not paciente:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Paciente no encontrado")
        return self.repo.por_paciente_cedula(paciente.id_paciente)
