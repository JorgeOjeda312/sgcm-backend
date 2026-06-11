from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Comprobante(Base):
    """RF-IE01 a RF-IE03: Emisión de comprobante, libro diario y conciliación contable."""
    __tablename__ = "comprobantes"

    id_comprobante = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas_medicas.id_consulta"), nullable=False)
    tipo = Column(String(30), nullable=False)  # factura / nota_de_venta
    numero_correlativo = Column(String(30), nullable=False, unique=True)
    total = Column(Float, nullable=False)
    estado = Column(String(20), default="PENDIENTE")  # pagado / pendiente
    fecha_emision = Column(DateTime, server_default=func.now())

    id_cuenta_contable = Column(Integer, ForeignKey("cuentas_contables.id_cuenta"), nullable=False)

    consulta = relationship("ConsultaMedica", back_populates="comprobantes")
    cuenta_contable = relationship("CuentaContable", back_populates="comprobantes")
