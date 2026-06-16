from sqlalchemy.orm import Session
from app.models.certificado import Certificado
from app.repositories.base_repository import BaseRepository


class CertificadoRepository(BaseRepository[Certificado]):
    def __init__(self, db: Session):
        super().__init__(Certificado, db)

    def ultimo_correlativo(self) -> int:
        total = self.db.query(Certificado).count()
        return total + 1
