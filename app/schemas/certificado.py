from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CertificadoBase(BaseModel):
    id_consulta: int
    tipo: str


class CertificadoCreate(CertificadoBase):
    pass


class CertificadoOut(CertificadoBase):
    model_config = ConfigDict(from_attributes=True)
    id_certificado: int
    numero_correlativo: str
    fecha_emision: datetime | None = None
