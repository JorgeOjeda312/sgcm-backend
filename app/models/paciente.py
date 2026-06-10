from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Paciente(Base):
    """RF-P01 a RF-P04: Registro, búsqueda, datos de facturación e historial clínico."""
    __tablename__ = "pacientes"

    id_paciente = Column(Integer, primary_key=True, index=True)
    cedula_pasaporte = Column(String(20), nullable=False, unique=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    sexo = Column(String(10), nullable=True)
    grupo_sanguineo = Column(String(5), nullable=True)
    alergias = Column(String(255), nullable=True)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    info_facturacion = Column(String(255), nullable=True)  # RF-P03: tercero responsable de pago

    citas = relationship("Cita", back_populates="paciente")
