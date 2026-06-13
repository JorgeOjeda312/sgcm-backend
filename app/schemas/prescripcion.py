from pydantic import BaseModel, ConfigDict


class PrescripcionBase(BaseModel):
    id_consulta: int
    medicamento: str
    dosis: str
    frecuencia: str
    duracion: str | None = None


class PrescripcionCreate(PrescripcionBase):
    pass


class PrescripcionOut(PrescripcionBase):
    model_config = ConfigDict(from_attributes=True)
    id_prescripcion: int
    impresa: bool
