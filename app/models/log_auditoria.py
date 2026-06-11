from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class LogAuditoria(Base):
    """RNF-06: Registro de auditoría de operaciones sobre datos clínicos."""
    __tablename__ = "logs_auditoria"

    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    accion = Column(String(20), nullable=False)  # CREAR / MODIFICAR / ELIMINAR
    tabla_afectada = Column(String(100), nullable=False)
    fecha_hora = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="logs")
