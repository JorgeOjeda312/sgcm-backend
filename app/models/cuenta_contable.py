from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class CuentaContable(Base):
    """RF-C04: Catálogo de cuentas contables para el módulo de Ingresos/Egresos."""
    __tablename__ = "cuentas_contables"

    id_cuenta = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre_cuenta = Column(String(150), nullable=False)
    tipo = Column(String(20), nullable=False)  # INGRESO / EGRESO

    comprobantes = relationship("Comprobante", back_populates="cuenta_contable")
