"""
Prueba de integración de extremo a extremo del API del SGCM.

Reproduce el flujo real descrito en la SRS (Tarea 02.01) y la DDS
(Tarea 02.02): configuración inicial, agendamiento de una cita, atención
médica, prescripción, orden de laboratorio, certificado médico y
facturación; verificando que las capas modelo / repositorio / servicio /
controlador funcionen correctamente integradas con una base de datos real
(SQLite de pruebas, ver tests/conftest.py).
"""


def test_flujo_completo_de_atencion_medica(client):
    # --- Configuración: rol, usuario y plan de cuentas (RF-C01 a RF-C04) ---
    rol = client.post("/roles/", json={"nombre_rol": "Médico"}).json()
    assert rol["id_rol"]

    usuario = client.post(
        "/usuarios/",
        json={
            "nombre": "Dra. Valeria Pérez",
            "correo": "vperez@consultorio.ec",
            "id_rol": rol["id_rol"],
            "contrasena": "ClaveSegura123",
        },
    ).json()
    assert "contrasena" not in usuario

    cuenta = client.post(
        "/cuentas-contables/",
        json={"codigo": "4101", "nombre_cuenta": "Ingresos por consultas", "tipo": "INGRESO"},
    ).json()

    # --- Colaboradores y pacientes (RF-CO01, RF-P01) ---
    medico = client.post(
        "/medicos/",
        json={
            "nombre_completo": "Dra. Valeria Pérez",
            "especialidad": "Medicina General",
            "registro_senescyt": "SEN-0001",
            "id_usuario": usuario["id_usuario"],
        },
    ).json()

    paciente = client.post(
        "/pacientes/",
        json={
            "cedula_pasaporte": "0102030405",
            "nombre_completo": "Jorge Ojeda",
            "telefono": "0991234567",
        },
    ).json()

    # --- Agenda de citas (RF-A01 a RF-A03) ---
    cita = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-07-01T09:00:00",
            "motivo_consulta": "Control general",
        },
    ).json()
    assert cita["estado"] == "PENDIENTE"

    # No se permite agendar dos citas en el mismo horario para el médico (RF-A02).
    conflicto = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-07-01T09:00:00",
        },
    )
    assert conflicto.status_code == 409

    disponibilidad = client.get(
        "/citas/disponibilidad",
        params={"id_medico": medico["id_medico"], "fecha": "2026-07-01"},
    )
    assert disponibilidad.status_code == 200
    assert len(disponibilidad.json()) == 1

    # --- Máquina de estados de la cita ---
    confirmada = client.patch(f"/citas/{cita['id_cita']}/confirmar").json()
    assert confirmada["estado"] == "CONFIRMADA"

    en_atencion = client.patch(f"/citas/{cita['id_cita']}/iniciar-atencion").json()
    assert en_atencion["estado"] == "EN_ATENCION"

    # --- Consulta médica, prescripción y orden (RF-M01 a RF-M03) ---
    consulta = client.post(
        "/consultas/",
        json={
            "id_cita": cita["id_cita"],
            "diagnostico_cie10": "J00",
            "plan_tratamiento": "Reposo e hidratación",
        },
    ).json()

    prescripcion = client.post(
        "/prescripciones/",
        json={
            "id_consulta": consulta["id_consulta"],
            "medicamento": "Paracetamol",
            "dosis": "500mg",
            "frecuencia": "cada 8 horas",
            "duracion": "5 días",
        },
    ).json()
    assert prescripcion["impresa"] is False

    impresa = client.patch(f"/prescripciones/{prescripcion['id_prescripcion']}/imprimir").json()
    assert impresa["impresa"] is True

    orden = client.post(
        "/ordenes-medicas/",
        json={
            "id_consulta": consulta["id_consulta"],
            "tipo": "Laboratorio",
            "descripcion": "Biometría hemática",
        },
    ).json()
    assert orden["id_orden"]

    certificado = client.post(
        "/certificados/",
        json={"id_consulta": consulta["id_consulta"], "tipo": "reposo"},
    ).json()
    assert certificado["numero_correlativo"].startswith("CERT-")

    finalizada = client.patch(f"/citas/{cita['id_cita']}/finalizar-atencion").json()
    assert finalizada["estado"] == "ATENDIDA"

    # --- Historial clínico (RF-P04 / RF-R02) ---
    historial = client.get(f"/pacientes/{paciente['id_paciente']}/historial")
    assert historial.status_code == 200
    assert len(historial.json()) == 1

    # --- Ingresos y egresos / reportes (RF-IE01 a RF-IE03, RF-R01, RF-R03) ---
    comprobante = client.post(
        "/comprobantes/",
        json={
            "id_consulta": consulta["id_consulta"],
            "tipo": "nota_de_venta",
            "total": 25.0,
            "id_cuenta_contable": cuenta["id_cuenta"],
        },
    ).json()
    assert comprobante["estado"] == "PENDIENTE"

    pagado = client.patch(f"/comprobantes/{comprobante['id_comprobante']}/pagar").json()
    assert pagado["estado"] == "PAGADO"

    libro_diario = client.get(
        "/reportes/libro-diario", params={"desde": "2020-01-01", "hasta": "2030-12-31"}
    )
    assert libro_diario.status_code == 200
    assert len(libro_diario.json()) == 1

    resumen = client.get(
        "/reportes/resumen-comprobantes", params={"desde": "2020-01-01", "hasta": "2030-12-31"}
    )
    assert resumen.status_code == 200
    assert resumen.json()["total_periodo"] == 25.0

    # --- Servicio web público de consulta de citas por cédula (RF-A05) ---
    consulta_publica = client.get(f"/citas/publico/por-cedula/{paciente['cedula_pasaporte']}")
    assert consulta_publica.status_code == 200
    assert consulta_publica.json()[0]["estado"] == "ATENDIDA"

    # --- Cancelación de una segunda cita (RF-A03) ---
    segunda_cita = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-07-02T10:00:00",
        },
    ).json()
    cancelada = client.patch(
        f"/citas/{segunda_cita['id_cita']}/cancelar",
        json={"motivo_cancelacion": "El paciente reprogramó"},
    ).json()
    assert cancelada["estado"] == "CANCELADA"
