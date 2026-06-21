"""
Carga datos de ejemplo en la base de datos para poder probar la API
manualmente desde Swagger UI (/docs) sin tener que crear todo desde cero.

Uso:
    python seed.py
"""
from datetime import date, datetime

from app.core.database import Base, engine, SessionLocal
import app.models as m

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if db.query(m.Rol).count() == 0:
        roles = [
            m.Rol(nombre_rol="Administrador", descripcion="Acceso total al sistema"),
            m.Rol(nombre_rol="Medico", descripcion="Atención clínica"),
            m.Rol(nombre_rol="Recepcionista", descripcion="Gestión de agenda y pacientes"),
            m.Rol(nombre_rol="Contador", descripcion="Gestión de ingresos y egresos"),
        ]
        db.add_all(roles)
        db.commit()
        print(f"Roles creados: {len(roles)}")

    if db.query(m.Medico).count() == 0:
        medicos = [
            m.Medico(
                nombre_completo="Dra. Ana López",
                especialidad="Medicina General",
                registro_senescyt="SEN-0001",
                horario_atencion="Lunes a Viernes 08:00-13:00",
                consultorio_asignado="Consultorio 1",
            ),
            m.Medico(
                nombre_completo="Dr. Carlos Mejía",
                especialidad="Pediatría",
                registro_senescyt="SEN-0002",
                horario_atencion="Lunes a Viernes 14:00-18:00",
                consultorio_asignado="Consultorio 2",
            ),
        ]
        db.add_all(medicos)
        db.commit()
        print(f"Médicos creados: {len(medicos)}")

    if db.query(m.Paciente).count() == 0:
        pacientes = [
            m.Paciente(
                cedula_pasaporte="0912345678",
                nombre_completo="Juan Pérez",
                fecha_nacimiento=date(1995, 4, 12),
                sexo="M",
                grupo_sanguineo="O+",
                telefono="0991234567",
            ),
            m.Paciente(
                cedula_pasaporte="0987654321",
                nombre_completo="María Torres",
                fecha_nacimiento=date(1988, 9, 23),
                sexo="F",
                grupo_sanguineo="A+",
                telefono="0987651234",
            ),
        ]
        db.add_all(pacientes)
        db.commit()
        print(f"Pacientes creados: {len(pacientes)}")

    if db.query(m.CuentaContable).count() == 0:
        cuentas = [
            m.CuentaContable(codigo="4001", nombre_cuenta="Ingresos por consulta médica", tipo="INGRESO"),
            m.CuentaContable(codigo="5001", nombre_cuenta="Gastos administrativos", tipo="EGRESO"),
        ]
        db.add_all(cuentas)
        db.commit()
        print(f"Cuentas contables creadas: {len(cuentas)}")

    print("Datos de ejemplo cargados correctamente. Abre /docs para probarlos.")
finally:
    db.close()
