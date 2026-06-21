from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.prescripcion_service import PrescripcionService
from app.schemas.prescripcion import PrescripcionCreate, PrescripcionOut

router = APIRouter(prefix="/prescripciones", tags=["Consultas Médicas - Prescripciones"])


@router.get("/por-consulta/{id_consulta}", response_model=list[PrescripcionOut])
def listar_por_consulta(id_consulta: int, db: Session = Depends(get_db)):
    return PrescripcionService(db).listar_por_consulta(id_consulta)


@router.post("/", response_model=PrescripcionOut, status_code=201)
def crear_prescripcion(data: PrescripcionCreate, db: Session = Depends(get_db)):
    """RF-M02: receta con medicamento, dosis, frecuencia y duración."""
    return PrescripcionService(db).crear(data)


@router.patch("/{id_prescripcion}/imprimir", response_model=PrescripcionOut)
def marcar_impresa(id_prescripcion: int, db: Session = Depends(get_db)):
    return PrescripcionService(db).marcar_impresa(id_prescripcion)
