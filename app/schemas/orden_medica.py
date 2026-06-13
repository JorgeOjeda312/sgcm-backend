from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OrdenMedicaBase(BaseModel):
    id_consulta: int
    tipo: str
    descripcion: str


class OrdenMedicaCreate(OrdenMedicaBase):
    pass


class OrdenMedicaOut(OrdenMedicaBase):
    model_config = ConfigDict(from_attributes=True)
    id_orden: int
    fecha_emision: datetime | None = None
