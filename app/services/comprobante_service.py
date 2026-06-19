from datetime import datetime, date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.comprobante import Comprobante
from app.repositories.comprobante_repository import ComprobanteRepository
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.schemas.comprobante import ComprobanteCreate


class ComprobanteService:
    """RF-IE01 a RF-IE03: emisión de comprobantes, libro diario y conciliación automática."""

    def __init__(self, db: Session):
        self.repo = ComprobanteRepository(db)
        self.consultas = ConsultaRepository(db)
        self.cuentas = CuentaRepository(db)

    def listar(self):
        return self.repo.list()

    def crear(self, data: ComprobanteCreate) -> Comprobante:
        """RF-IE01 + RF-IE03: emite el comprobante validando consulta y cuenta contable."""
        if not self.consultas.get(data.id_consulta):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta no encontrada")
        if not self.cuentas.get(data.id_cuenta_contable):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cuenta contable no encontrada")

        correlativo = f"NV-{datetime.now().year}-{self.repo.ultimo_correlativo():06d}"
        comprobante = Comprobante(
            id_consulta=data.id_consulta,
            tipo=data.tipo,
            total=data.total,
            id_cuenta_contable=data.id_cuenta_contable,
            numero_correlativo=correlativo,
            estado="PENDIENTE",
        )
        return self.repo.create(comprobante)

    def marcar_pagado(self, id_comprobante: int) -> Comprobante:
        comprobante = self.repo.get(id_comprobante)
        if not comprobante:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Comprobante no encontrado")
        return self.repo.update(comprobante, {"estado": "PAGADO"})

    def libro_diario(self, desde: date, hasta: date):
        """RF-R01: reporte de movimientos contables en un rango de fechas."""
        return self.repo.por_rango_fecha(desde, hasta)

    def resumen_comprobantes(self, desde: date, hasta: date):
        """RF-R03: resumen de comprobantes filtrable por fecha."""
        comprobantes = self.repo.por_rango_fecha(desde, hasta)
        total = sum(c.total for c in comprobantes)
        return {"comprobantes": comprobantes, "total_periodo": total}
