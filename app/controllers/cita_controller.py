from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cita_service import CitaService
from app.schemas.cita import CitaCreate, CitaOut, CitaCancelar

router = APIRouter(prefix="/citas", tags=["Agenda de Citas"])


@router.get("/", response_model=list[CitaOut])
def listar_citas(db: Session = Depends(get_db)):
    return CitaService(db).listar()


@router.get("/disponibilidad", response_model=list[str])
def disponibilidad(id_medico: int, fecha: date, db: Session = Depends(get_db)):
    """RF-A01: slots ocupados de un médico en una fecha (ISO 8601)."""
    ocupados = CitaService(db).disponibilidad(id_medico, fecha)
    return [f.isoformat() for f in ocupados]


@router.get("/{id_cita}", response_model=CitaOut)
def obtener_cita(id_cita: int, db: Session = Depends(get_db)):
    return CitaService(db).obtener(id_cita)


@router.post("/", response_model=CitaOut, status_code=201)
def agendar_cita(data: CitaCreate, db: Session = Depends(get_db)):
    """RF-A02: reserva de cita validando disponibilidad del médico."""
    return CitaService(db).agendar(data)


@router.patch("/{id_cita}/confirmar", response_model=CitaOut)
def confirmar_cita(id_cita: int, db: Session = Depends(get_db)):
    return CitaService(db).confirmar(id_cita)


@router.patch("/{id_cita}/iniciar-atencion", response_model=CitaOut)
def iniciar_atencion(id_cita: int, db: Session = Depends(get_db)):
    return CitaService(db).iniciar_atencion(id_cita)


@router.patch("/{id_cita}/finalizar-atencion", response_model=CitaOut)
def finalizar_atencion(id_cita: int, db: Session = Depends(get_db)):
    return CitaService(db).finalizar_atencion(id_cita)


@router.patch("/{id_cita}/cancelar", response_model=CitaOut)
def cancelar_cita(id_cita: int, data: CitaCancelar, db: Session = Depends(get_db)):
    """RF-A03: cancelación de cita registrando el motivo."""
    return CitaService(db).cancelar(id_cita, data)


@router.get("/publico/por-cedula/{cedula}", response_model=list[CitaOut])
def consulta_publica(cedula: str, db: Session = Depends(get_db)):
    """RF-A05: servicio web REST de consulta de citas por cédula del paciente."""
    return CitaService(db).consulta_publica_por_cedula(cedula)
