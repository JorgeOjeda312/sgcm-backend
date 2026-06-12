from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    id_rol: int
    estado_activo: bool = True


class UsuarioCreate(UsuarioBase):
    contrasena: str  # texto plano de entrada; se hashea en el servicio (RNF-04)


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: EmailStr | None = None
    id_rol: int | None = None
    estado_activo: bool | None = None


class UsuarioOut(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: int
    fecha_creacion: datetime | None = None
