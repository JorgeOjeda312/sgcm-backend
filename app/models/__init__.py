"""
Centraliza la importación de todos los modelos para que SQLAlchemy
pueda resolver las relaciones declaradas por nombre de clase (string)
antes de llamar a Base.metadata.create_all().
"""
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.cita import Cita, EstadoCita
from app.models.consulta_medica import ConsultaMedica
from app.models.prescripcion import Prescripcion
from app.models.orden_medica import OrdenMedica
from app.models.certificado import Certificado
from app.models.cuenta_contable import CuentaContable
from app.models.comprobante import Comprobante
from app.models.log_auditoria import LogAuditoria

__all__ = [
    "Rol", "Usuario", "Paciente", "Medico", "Cita", "EstadoCita",
    "ConsultaMedica", "Prescripcion", "OrdenMedica", "Certificado",
    "CuentaContable", "Comprobante", "LogAuditoria",
]
