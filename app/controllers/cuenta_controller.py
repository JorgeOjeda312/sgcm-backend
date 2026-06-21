from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cuenta_service import CuentaService
from app.schemas.cuenta_contable import CuentaContableCreate, CuentaContableOut

router = APIRouter(prefix="/cuentas-contables", tags=["Ingresos y Egresos - Plan de Cuentas"])


@router.get("/", response_model=list[CuentaContableOut])
def listar_cuentas(db: Session = Depends(get_db)):
    return CuentaService(db).listar()


@router.post("/", response_model=CuentaContableOut, status_code=201)
def crear_cuenta(data: CuentaContableCreate, db: Session = Depends(get_db)):
    """RF-C04: catálogo de cuentas contables."""
    return CuentaService(db).crear(data)
