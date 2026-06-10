from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Medico(Base):
    """RF-CO01, RF-CO03: Registro y consulta de médicos."""
    __tablename__ = "medicos"

    id_medico = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    especialidad = Column(String(100), nullable=False)
    registro_senescyt = Column(String(50), nullable=False, unique=True)
    horario_atencion = Column(String(255), nullable=True)
    consultorio_asignado = Column(String(50), nullable=True)

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    usuario = relationship("Usuario", back_populates="medico")

    citas = relationship("Cita", back_populates="medico")
