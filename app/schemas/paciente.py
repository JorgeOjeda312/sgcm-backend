from pydantic import BaseModel, ConfigDict
from datetime import date


class PacienteBase(BaseModel):
    cedula_pasaporte: str
    nombre_completo: str
    fecha_nacimiento: date | None = None
    sexo: str | None = None
    grupo_sanguineo: str | None = None
    alergias: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    info_facturacion: str | None = None


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    nombre_completo: str | None = None
    fecha_nacimiento: date | None = None
    sexo: str | None = None
    grupo_sanguineo: str | None = None
    alergias: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    info_facturacion: str | None = None


class PacienteOut(PacienteBase):
    model_config = ConfigDict(from_attributes=True)
    id_paciente: int
