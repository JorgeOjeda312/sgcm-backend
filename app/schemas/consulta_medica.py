from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ConsultaMedicaBase(BaseModel):
    id_cita: int
    anamnesis: str | None = None
    examen_fisico: str | None = None
    diagnostico_cie10: str | None = None
    plan_tratamiento: str | None = None


class ConsultaMedicaCreate(ConsultaMedicaBase):
    pass


class ConsultaMedicaUpdate(BaseModel):
    anamnesis: str | None = None
    examen_fisico: str | None = None
    diagnostico_cie10: str | None = None
    plan_tratamiento: str | None = None


class ConsultaMedicaOut(ConsultaMedicaBase):
    model_config = ConfigDict(from_attributes=True)
    id_consulta: int
    fecha_registro: datetime | None = None
