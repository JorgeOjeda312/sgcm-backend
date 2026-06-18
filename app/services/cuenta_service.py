from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.cuenta_contable import CuentaContable
from app.repositories.cuenta_repository import CuentaRepository
from app.schemas.cuenta_contable import CuentaContableCreate


class CuentaService:
    """RF-C04: catálogo de cuentas contables."""

    def __init__(self, db: Session):
        self.repo = CuentaRepository(db)

    def listar(self):
        return self.repo.list()

    def crear(self, data: CuentaContableCreate) -> CuentaContable:
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El código de cuenta ya existe")
        return self.repo.create(CuentaContable(**data.model_dump()))
