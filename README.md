# SGCM — Sistema de Gestión de Citas Médicas

Backend de la **Tarea 02.03 — Construcción de aplicación de software**, materia
Ingeniería de Software, Universidad Politécnica Salesiana (Sede Guayaquil).

**Grupo:** Innovasoft
**Integrantes:** Jorge Ojeda · Cristhian Veloz · Domenica Franco · Martha Cárdenas

Este servicio implementa el backend del SGCM descrito en la **Especificación de
Requerimientos de Software (SRS — Tarea 02.01)** y la **Descripción de Diseño
de Software (DDS — Tarea 02.02)** elaboradas previamente por el grupo. Los
documentos de referencia se encuentran en [`docs/`](docs/).

## 1. Arquitectura

Se utiliza el esquema **modelo → repositorio → servicio → controlador**
solicitado en la guía de la tarea:

```
app/
├── models/         # Entidades SQLAlchemy (capa de datos / ORM)
├── schemas/        # Esquemas Pydantic de entrada/salida (DTOs)
├── repositories/    # Acceso a datos (patrón Repository)
├── services/        # Reglas de negocio y validaciones
├── controllers/      # Routers de FastAPI (capa de presentación de la API)
└── main.py            # Punto de entrada, ensamblado de routers y Swagger
```

- **Modelo (`models/`):** clases que reflejan el Diagrama de Clases y el
  Diagrama Entidad-Relación de la DDS: `Rol`, `Usuario`, `Paciente`, `Medico`,
  `Cita`, `ConsultaMedica`, `Prescripcion`, `OrdenMedica`, `Certificado`,
  `Comprobante`, `CuentaContable`, `LogAuditoria`.
- **Repositorio (`repositories/`):** encapsula las consultas SQL/ORM (CRUD
  genérico + consultas específicas como búsqueda por cédula o verificación de
  disponibilidad de horarios).
- **Servicio (`services/`):** contiene las reglas de negocio, por ejemplo la
  máquina de estados de la `Cita` (`PENDIENTE → CONFIRMADA → EN_ATENCION →
  ATENDIDA`, con `CANCELADA`/`NO_PRESENTADA` como estados alternos), tal como
  se definió en el Diagrama de Estados de la DDS.
- **Controlador (`controllers/`):** routers de FastAPI que exponen los
  endpoints REST y delegan en los servicios.

## 2. Trazabilidad con la SRS (resumen)

| Módulo SRS | Endpoints principales |
| --- | --- |
| Configuración (RF-C01, RF-C02, RF-C04) | `/usuarios`, `/roles`, `/cuentas-contables` |
| Pacientes (RF-P01–RF-P04) | `/pacientes`, `/pacientes/buscar`, `/pacientes/{id}/historial` |
| Colaboradores (RF-CO01–RF-CO03) | `/medicos`, `/medicos/buscar` |
| Agenda de Citas (RF-A01–RF-A05) | `/citas`, `/citas/disponibilidad`, `/citas/publico/por-cedula/{cedula}` |
| Consultas Médicas (RF-M01–RF-M03) | `/consultas`, `/prescripciones`, `/ordenes-medicas` |
| Certificados (RF-CE01) | `/certificados` |
| Ingresos y Egresos (RF-IE01–RF-IE03) | `/comprobantes` |
| Reportes (RF-R01–RF-R03) | `/reportes/libro-diario`, `/reportes/resumen-comprobantes`, `/pacientes/{id}/historial` |

## 3. Ejecución local

```bash
python3 -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Opcional) cargar datos de ejemplo
python seed.py

uvicorn app.main:app --reload
```

- API: <http://localhost:8000>
- **Swagger UI:** <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Esquema OpenAPI: <http://localhost:8000/openapi.json>

Por defecto se usa SQLite (`sgcm.db`) para facilitar la evaluación sin
infraestructura adicional. Para usar PostgreSQL (como define la SRS), basta
con definir la variable de entorno `DATABASE_URL`, por ejemplo:

```bash
export DATABASE_URL="postgresql://usuario:clave@localhost:5432/sgcm"
```

## 4. Ejecución con Docker

```bash
docker build -t sgcm-backend .
docker run -p 8000:8000 sgcm-backend
```

## 5. Seguimiento de tareas del equipo

Las tareas se gestionaron mediante el tablero de *Issues* del repositorio
(ver [`TASKS.md`](TASKS.md) para el resumen de asignaciones por integrante).

## 6. Documentos de diseño

- [`docs/SRS_Sistema_Gestion_Citas_Medicas.pdf`](docs/SRS_Sistema_Gestion_Citas_Medicas.pdf) — Tarea 02.01
- [`docs/DDS_Sistema_Gestion_Citas_Medicas.pdf`](docs/DDS_Sistema_Gestion_Citas_Medicas.pdf) — Tarea 02.02

## 7. Pruebas rápidas con curl

```bash
curl -X POST http://localhost:8000/roles/ \
  -H "Content-Type: application/json" \
  -d '{"nombre_rol": "Administrador", "descripcion": "Acceso total"}'

curl http://localhost:8000/pacientes/
```
