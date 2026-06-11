from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class OrdenMedica(Base):
    """RF-M03: Órdenes de laboratorio, imagen u otros procedimientos."""
    __tablename__ = "ordenes_medicas"

    id_orden = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas_medicas.id_consulta"), nullable=False)
    tipo = Column(String(50), nullable=False)  # laboratorio, imagen, otro
    descripcion = Column(String(500), nullable=False)
    fecha_emision = Column(DateTime, server_default=func.now())

    consulta = relationship("ConsultaMedica", back_populates="ordenes")
