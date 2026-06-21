from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.orden_service import OrdenService
from app.schemas.orden_medica import OrdenMedicaCreate, OrdenMedicaOut

router = APIRouter(prefix="/ordenes-medicas", tags=["Consultas Médicas - Órdenes"])


@router.get("/por-consulta/{id_consulta}", response_model=list[OrdenMedicaOut])
def listar_por_consulta(id_consulta: int, db: Session = Depends(get_db)):
    return OrdenService(db).listar_por_consulta(id_consulta)


@router.post("/", response_model=OrdenMedicaOut, status_code=201)
def crear_orden(data: OrdenMedicaCreate, db: Session = Depends(get_db)):
    """RF-M03: órdenes de laboratorio, imagen u otros procedimientos."""
    return OrdenService(db).crear(data)
