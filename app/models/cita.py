import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class EstadoCita(str, enum.Enum):
    """Ciclo de vida de la cita, según el Diagrama de Estados de la Tarea 02.02 (IEEE 1016)."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    EN_ATENCION = "EN_ATENCION"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"
    NO_PRESENTADA = "NO_PRESENTADA"


class Cita(Base):
    """RF-A01 a RF-A05: Calendario, reserva, cancelación, notificación y servicio web."""
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    motivo_consulta = Column(String(255), nullable=True)
    estado = Column(Enum(EstadoCita), default=EstadoCita.PENDIENTE, nullable=False)
    motivo_cancelacion = Column(String(255), nullable=True)
    notificacion_enviada = Column(Boolean, default=False)

    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
    consulta = relationship("ConsultaMedica", back_populates="cita", uselist=False)
