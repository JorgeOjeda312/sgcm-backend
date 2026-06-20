from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.medico_service import MedicoService
from app.schemas.medico import MedicoCreate, MedicoUpdate, MedicoOut

router = APIRouter(prefix="/medicos", tags=["Colaboradores - Médicos"])


@router.get("/", response_model=list[MedicoOut])
def listar_medicos(db: Session = Depends(get_db)):
    return MedicoService(db).listar()


@router.get("/buscar", response_model=list[MedicoOut])
def buscar_medicos(
    nombre: str | None = Query(None),
    especialidad: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """RF-CO03: búsqueda y filtrado de colaboradores por nombre o especialidad."""
    return MedicoService(db).buscar(nombre, especialidad)


@router.get("/{id_medico}", response_model=MedicoOut)
def obtener_medico(id_medico: int, db: Session = Depends(get_db)):
    return MedicoService(db).obtener(id_medico)


@router.post("/", response_model=MedicoOut, status_code=201)
def crear_medico(data: MedicoCreate, db: Session = Depends(get_db)):
    return MedicoService(db).crear(data)


@router.put("/{id_medico}", response_model=MedicoOut)
def actualizar_medico(id_medico: int, data: MedicoUpdate, db: Session = Depends(get_db)):
    return MedicoService(db).actualizar(id_medico, data)


@router.delete("/{id_medico}", status_code=204)
def eliminar_medico(id_medico: int, db: Session = Depends(get_db)):
    MedicoService(db).eliminar(id_medico)
