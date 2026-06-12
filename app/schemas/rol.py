from pydantic import BaseModel, ConfigDict


class RolBase(BaseModel):
    nombre_rol: str
    descripcion: str | None = None


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre_rol: str | None = None
    descripcion: str | None = None


class RolOut(RolBase):
    model_config = ConfigDict(from_attributes=True)
    id_rol: int
