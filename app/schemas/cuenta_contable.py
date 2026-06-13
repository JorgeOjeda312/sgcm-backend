from pydantic import BaseModel, ConfigDict


class CuentaContableBase(BaseModel):
    codigo: str
    nombre_cuenta: str
    tipo: str  # INGRESO / EGRESO


class CuentaContableCreate(CuentaContableBase):
    pass


class CuentaContableOut(CuentaContableBase):
    model_config = ConfigDict(from_attributes=True)
    id_cuenta: int
