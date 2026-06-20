from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.paciente_service import PacienteService
from app.services.consulta_service import ConsultaService
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteOut
from app.schemas.consulta_medica import ConsultaMedicaOut

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=list[PacienteOut])
def listar_pacientes(db: Session = Depends(get_db)):
    return PacienteService(db).listar()


@router.get("/buscar", response_model=list[PacienteOut])
def buscar_pacientes(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    """RF-P02: búsqueda por cédula, nombre o apellido."""
    return PacienteService(db).buscar(q)


@router.get("/{id_paciente}", response_model=PacienteOut)
def obtener_paciente(id_paciente: int, db: Session = Depends(get_db)):
    return PacienteService(db).obtener(id_paciente)


@router.get("/{id_paciente}/historial", response_model=list[ConsultaMedicaOut])
def historial_clinico(id_paciente: int, db: Session = Depends(get_db)):
    """RF-P04 / RF-R02: historial clínico cronológico del paciente."""
    return ConsultaService(db).historial_de_paciente(id_paciente)


@router.post("/", response_model=PacienteOut, status_code=201)
def crear_paciente(data: PacienteCreate, db: Session = Depends(get_db)):
    return PacienteService(db).crear(data)


@router.put("/{id_paciente}", response_model=PacienteOut)
def actualizar_paciente(id_paciente: int, data: PacienteUpdate, db: Session = Depends(get_db)):
    return PacienteService(db).actualizar(id_paciente, data)


@router.delete("/{id_paciente}", status_code=204)
def eliminar_paciente(id_paciente: int, db: Session = Depends(get_db)):
    PacienteService(db).eliminar(id_paciente)
