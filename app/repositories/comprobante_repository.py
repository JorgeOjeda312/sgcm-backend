from datetime import date, datetime, time
from sqlalchemy.orm import Session
from app.models.comprobante import Comprobante
from app.repositories.base_repository import BaseRepository


class ComprobanteRepository(BaseRepository[Comprobante]):
    """RF-R01, RF-R03: Soporte para libro diario y resumen de comprobantes."""

    def __init__(self, db: Session):
        super().__init__(Comprobante, db)

    def ultimo_correlativo(self) -> int:
        return self.db.query(Comprobante).count() + 1

    def por_rango_fecha(self, desde: date, hasta: date) -> list[Comprobante]:
        inicio = datetime.combine(desde, time.min)
        fin = datetime.combine(hasta, time.max)
        return (
            self.db.query(Comprobante)
            .filter(Comprobante.fecha_emision.between(inicio, fin))
            .all()
        )
