from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.cita import EstadoCita


class CitaBase(BaseModel):
    id_paciente: int
    id_medico: int
    fecha_hora: datetime
    motivo_consulta: str | None = None


class CitaCreate(CitaBase):
    pass


class CitaCancelar(BaseModel):
    motivo_cancelacion: str


class CitaOut(CitaBase):
    model_config = ConfigDict(from_attributes=True)
    id_cita: int
    estado: EstadoCita
    motivo_cancelacion: str | None = None
    notificacion_enviada: bool
