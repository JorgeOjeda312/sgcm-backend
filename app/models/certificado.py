from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Certificado(Base):
    """RF-CE01: Emisión de certificados médicos (reposo, salud o personalizado)."""
    __tablename__ = "certificados"

    id_certificado = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas_medicas.id_consulta"), nullable=False)
    tipo = Column(String(50), nullable=False)  # reposo, salud, personalizado
    numero_correlativo = Column(String(30), nullable=False, unique=True)
    fecha_emision = Column(DateTime, server_default=func.now())

    consulta = relationship("ConsultaMedica", back_populates="certificados")
