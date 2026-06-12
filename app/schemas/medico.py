from pydantic import BaseModel, ConfigDict


class MedicoBase(BaseModel):
    nombre_completo: str
    especialidad: str
    registro_senescyt: str
    horario_atencion: str | None = None
    consultorio_asignado: str | None = None
    id_usuario: int | None = None


class MedicoCreate(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    nombre_completo: str | None = None
    especialidad: str | None = None
    horario_atencion: str | None = None
    consultorio_asignado: str | None = None


class MedicoOut(MedicoBase):
    model_config = ConfigDict(from_attributes=True)
    id_medico: int
