from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.comprobante_service import ComprobanteService
from app.schemas.comprobante import ComprobanteCreate, ComprobanteOut

router = APIRouter(prefix="/comprobantes", tags=["Ingresos y Egresos - Comprobantes"])


@router.get("/", response_model=list[ComprobanteOut])
def listar_comprobantes(db: Session = Depends(get_db)):
    return ComprobanteService(db).listar()


@router.post("/", response_model=ComprobanteOut, status_code=201)
def emitir_comprobante(data: ComprobanteCreate, db: Session = Depends(get_db)):
    """RF-IE01 + RF-IE03: emisión de comprobante con conciliación automática de cuenta."""
    return ComprobanteService(db).crear(data)


@router.patch("/{id_comprobante}/pagar", response_model=ComprobanteOut)
def marcar_pagado(id_comprobante: int, db: Session = Depends(get_db)):
    return ComprobanteService(db).marcar_pagado(id_comprobante)


reportes_router = APIRouter(prefix="/reportes", tags=["Reportes"])


@reportes_router.get("/libro-diario", response_model=list[ComprobanteOut])
def libro_diario(desde: date, hasta: date, db: Session = Depends(get_db)):
    """RF-R01: reporte de movimientos contables en un rango de fechas."""
    return ComprobanteService(db).libro_diario(desde, hasta)


@reportes_router.get("/resumen-comprobantes")
def resumen_comprobantes(desde: date, hasta: date, db: Session = Depends(get_db)):
    """RF-R03: resumen de comprobantes filtrable por fecha."""
    return ComprobanteService(db).resumen_comprobantes(desde, hasta)
