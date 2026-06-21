from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.certificado_service import CertificadoService
from app.schemas.certificado import CertificadoCreate, CertificadoOut

router = APIRouter(prefix="/certificados", tags=["Certificados"])


@router.get("/", response_model=list[CertificadoOut])
def listar_certificados(db: Session = Depends(get_db)):
    return CertificadoService(db).listar()


@router.post("/", response_model=CertificadoOut, status_code=201)
def emitir_certificado(data: CertificadoCreate, db: Session = Depends(get_db)):
    """RF-CE01: certificados de reposo, salud o personalizados con numeración correlativa."""
    return CertificadoService(db).crear(data)
