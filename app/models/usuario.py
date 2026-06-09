from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Usuario(Base):
    """RF-C01: Gestión de usuarios del sistema."""
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    correo = Column(String(150), nullable=False, unique=True, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    estado_activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())

    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    rol = relationship("Rol", back_populates="usuarios")

    medico = relationship("Medico", back_populates="usuario", uselist=False)
    logs = relationship("LogAuditoria", back_populates="usuario")
