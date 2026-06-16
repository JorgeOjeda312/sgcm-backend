from sqlalchemy.orm import Session
from app.models.cuenta_contable import CuentaContable
from app.repositories.base_repository import BaseRepository


class CuentaRepository(BaseRepository[CuentaContable]):
    def __init__(self, db: Session):
        super().__init__(CuentaContable, db)

    def get_by_codigo(self, codigo: str) -> CuentaContable | None:
        return self.db.query(CuentaContable).filter(CuentaContable.codigo == codigo).first()
