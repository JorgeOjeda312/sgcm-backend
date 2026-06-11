from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Prescripcion(Base):
    """RF-M02: Prescripción médica (medicamento, dosis, frecuencia, duración)."""
    __tablename__ = "prescripciones"

    id_prescripcion = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas_medicas.id_consulta"), nullable=False)
    medicamento = Column(String(150), nullable=False)
    dosis = Column(String(50), nullable=False)
    frecuencia = Column(String(50), nullable=False)
    duracion = Column(String(50), nullable=True)
    impresa = Column(Boolean, default=False)

    consulta = relationship("ConsultaMedica", back_populates="prescripciones")
