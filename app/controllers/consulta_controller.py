from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.consulta_service import ConsultaService
from app.schemas.consulta_medica import ConsultaMedicaCreate, ConsultaMedicaUpdate, ConsultaMedicaOut

router = APIRouter(prefix="/consultas", tags=["Consultas Médicas"])


@router.get("/", response_model=list[ConsultaMedicaOut])
def listar_consultas(db: Session = Depends(get_db)):
    return ConsultaService(db).listar()


@router.get("/{id_consulta}", response_model=ConsultaMedicaOut)
def obtener_consulta(id_consulta: int, db: Session = Depends(get_db)):
    return ConsultaService(db).obtener(id_consulta)


@router.post("/", response_model=ConsultaMedicaOut, status_code=201)
def registrar_consulta(data: ConsultaMedicaCreate, db: Session = Depends(get_db)):
    """RF-M01: anamnesis, examen físico, diagnóstico CIE-10 y plan de tratamiento."""
    return ConsultaService(db).crear(data)


@router.put("/{id_consulta}", response_model=ConsultaMedicaOut)
def actualizar_consulta(id_consulta: int, data: ConsultaMedicaUpdate, db: Session = Depends(get_db)):
    return ConsultaService(db).actualizar(id_consulta, data)
