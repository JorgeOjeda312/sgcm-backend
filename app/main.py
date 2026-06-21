"""
Sistema de Gestión de Citas Médicas (SGCM) - Backend
Universidad Politécnica Salesiana - Grupo Innovasoft
Tarea 02.03 - Construcción de aplicación de software

Implementado siguiendo la SRS (Tarea 02.01) y la DDS (Tarea 02.02),
con arquitectura en capas: modelo -> repositorio -> servicio -> controlador.

Documentación interactiva (Swagger UI):  /docs
Documentación alternativa (ReDoc):        /redoc
Esquema OpenAPI:                          /openapi.json
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.models  # noqa: F401  (registra todos los modelos antes de create_all)

from app.controllers.rol_controller import router as rol_router
from app.controllers.usuario_controller import router as usuario_router
from app.controllers.paciente_controller import router as paciente_router
from app.controllers.medico_controller import router as medico_router
from app.controllers.cita_controller import router as cita_router
from app.controllers.consulta_controller import router as consulta_router
from app.controllers.prescripcion_controller import router as prescripcion_router
from app.controllers.orden_controller import router as orden_router
from app.controllers.certificado_controller import router as certificado_router
from app.controllers.cuenta_controller import router as cuenta_router
from app.controllers.comprobante_controller import (
    router as comprobante_router,
    reportes_router,
)

app = FastAPI(
    title="SGCM API - Sistema de Gestión de Citas Médicas",
    description=(
        "API REST del Sistema de Gestión de Citas Médicas (SGCM), desarrollada "
        "para el consultorio médico descrito en la SRS y la DDS del Grupo Innovasoft. "
        "Arquitectura en capas: modelo / repositorio / servicio / controlador."
    ),
    version="1.0.0",
    contact={"name": "Grupo Innovasoft - UPS Sede Guayaquil"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea las tablas si no existen (en producción se recomienda usar Alembic).
Base.metadata.create_all(bind=engine)

app.include_router(rol_router)
app.include_router(usuario_router)
app.include_router(paciente_router)
app.include_router(medico_router)
app.include_router(cita_router)
app.include_router(consulta_router)
app.include_router(prescripcion_router)
app.include_router(orden_router)
app.include_router(certificado_router)
app.include_router(cuenta_router)
app.include_router(comprobante_router)
app.include_router(reportes_router)


@app.get("/", tags=["Salud"])
def raiz():
    return {
        "sistema": "SGCM - Sistema de Gestión de Citas Médicas",
        "estado": "operativo",
        "documentacion": "/docs",
    }
