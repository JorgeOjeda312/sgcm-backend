from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ConsultaMedica(Base):
    """RF-M01: Registro de anamnesis, examen físico, diagnóstico CIE-10 y plan de tratamiento."""
    __tablename__ = "consultas_medicas"

    id_consulta = Column(Integer, primary_key=True, index=True)
    id_cita = Column(Integer, ForeignKey("citas.id_cita"), nullable=False, unique=True)
    anamnesis = Column(String(2000), nullable=True)
    examen_fisico = Column(String(2000), nullable=True)
    diagnostico_cie10 = Column(String(100), nullable=True)
    plan_tratamiento = Column(String(2000), nullable=True)
    fecha_registro = Column(DateTime, server_default=func.now())

    cita = relationship("Cita", back_populates="consulta")
    prescripciones = relationship("Prescripcion", back_populates="consulta")
    ordenes = relationship("OrdenMedica", back_populates="consulta")
    certificados = relationship("Certificado", back_populates="consulta")
    comprobantes = relationship("Comprobante", back_populates="consulta")
