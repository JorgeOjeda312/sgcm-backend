from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ComprobanteBase(BaseModel):
    id_consulta: int
    tipo: str  # factura / nota_de_venta
    total: float
    id_cuenta_contable: int


class ComprobanteCreate(ComprobanteBase):
    pass


class ComprobanteOut(ComprobanteBase):
    model_config = ConfigDict(from_attributes=True)
    id_comprobante: int
    numero_correlativo: str
    estado: str
    fecha_emision: datetime | None = None
