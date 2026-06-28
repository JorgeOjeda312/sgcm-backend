# Seguimiento de tareas — Grupo Innovasoft

Tablero de tareas del repositorio para la Tarea 02.03. Cada tarea fue
registrada como *Issue* en el repositorio y asignada a un integrante,
siguiendo lo solicitado en la instrucción 7.1 de la guía de la tarea.

| # | Tarea | Módulo / capa | Asignado a | Estado |
| --- | --- | --- | --- | --- |
| 1 | Definir estructura del proyecto y configuración de base de datos | `core/database.py` | Jorge Ojeda | Cerrado |
| 2 | Modelar entidades Usuario, Rol y Médico | `models/` | Jorge Ojeda | Cerrado |
| 3 | Modelar entidades Paciente, Cita y máquina de estados | `models/`, `services/cita_service.py` | Jorge Ojeda | Cerrado |
| 4 | Modelar entidades clínicas: ConsultaMedica, Prescripción, Orden, Certificado | `models/` | Cristhian Veloz | Cerrado |
| 5 | Modelar módulo contable: CuentaContable, Comprobante, LogAuditoria | `models/` | Cristhian Veloz | Cerrado |
| 6 | Repositorios (capa de acceso a datos) para todos los módulos | `repositories/` | Domenica Franco | Cerrado |
| 7 | Servicios y reglas de negocio (validaciones, disponibilidad de horarios) | `services/` | Domenica Franco | Cerrado |
| 8 | Controladores REST y documentación Swagger | `controllers/`, `main.py` | Martha Cárdenas | Cerrado |
| 9 | Endpoints de reportes (libro diario, historial clínico, resumen) | `controllers/comprobante_controller.py` | Martha Cárdenas | Cerrado |
| 10 | Pruebas funcionales end-to-end del flujo de agendamiento | Todo el equipo | Cerrado |
| 11 | Redacción de README, TASKS y despliegue | Documentación | Jorge Ojeda | Cerrado |

> Nota: actualizar el enlace a cada *Issue* del repositorio (`#1`, `#2`, ...)
> una vez creado en GitHub, y verificar que los commits reales del historial
> reflejen la participación de cada integrante (mínimo 20 commits en total).

## Tarea 02.04 — Pruebas unitarias

| # | Tarea | Módulo / capa | Asignado a | Estado |
| --- | --- | --- | --- | --- |
| 12 | Configurar Pytest, Coverage.py y `conftest.py` (base de datos de pruebas) | `tests/conftest.py`, `pytest.ini`, `.coveragerc` | Jorge Ojeda | Cerrado |
| 13 | Pruebas unitarias de Cita (máquina de estados) y Consulta | `tests/unit/test_cita_service.py`, `test_consulta_service.py` | Jorge Ojeda | Cerrado |
| 14 | Pruebas unitarias de Prescripción, Orden, Certificado y Cuenta Contable | `tests/unit/test_prescripcion_service.py`, `test_orden_service.py`, `test_certificado_service.py`, `test_cuenta_service.py` | Cristhian Veloz | Cerrado |
| 15 | Pruebas unitarias de Usuario (hash de contraseña + doctest) y Rol | `tests/unit/test_usuario_service.py`, `test_rol_service.py`, `tests/test_doctests.py` | Domenica Franco | Cerrado |
| 16 | Pruebas unitarias de Paciente, Médico y Comprobante | `tests/unit/test_paciente_service.py`, `test_medico_service.py`, `test_comprobante_service.py` | Martha Cárdenas | Cerrado |
| 17 | Pruebas de integración: BaseRepository y flujo completo del API | `tests/integration/` | Todo el equipo | Cerrado |

> Nota: al subir estas pruebas, hacer **al menos un commit por tarea de la
> tabla anterior** (idealmente uno por archivo de prueba) en lugar de un
> único commit masivo, para cumplir el criterio de la rúbrica de T02.04 de
> *"al menos 10 commits que aseguren que han trabajado todos los
> compañeros"*.
