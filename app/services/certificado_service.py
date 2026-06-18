from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.certificado import Certificado
from app.repositories.certificado_repository import CertificadoRepository
from app.repositories.consulta_repository import ConsultaRepository
from app.schemas.certificado import CertificadoCreate


class CertificadoService:
    """RF-CE01: emisión de certificados médicos con numeración correlativa."""

    def __init__(self, db: Session):
        self.repo = CertificadoRepository(db)
        self.consultas = ConsultaRepository(db)

    def listar(self):
        return self.repo.list()

    def crear(self, data: CertificadoCreate) -> Certificado:
        if not self.consultas.get(data.id_consulta):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta no encontrada")
        correlativo = f"CERT-{datetime.now().year}-{self.repo.ultimo_correlativo():05d}"
        certificado = Certificado(
            id_consulta=data.id_consulta,
            tipo=data.tipo,
            numero_correlativo=correlativo,
        )
        return self.repo.create(certificado)
