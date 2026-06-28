"""
Pruebas de integración de validaciones y rutas de error del API del SGCM.

Complementan el flujo feliz de test_api_flujo_completo.py cubriendo
operaciones de listado, búsqueda, actualización y eliminación, así como
los códigos de error (400/404/409) que debe responder cada controlador.
"""


def test_endpoint_raiz_responde_ok(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "operativo"


def test_listar_roles_vacio(client):
    respuesta = client.get("/roles/")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_rol_duplicado_devuelve_400(client):
    client.post("/roles/", json={"nombre_rol": "Recepcionista"})
    respuesta = client.post("/roles/", json={"nombre_rol": "Recepcionista"})
    assert respuesta.status_code == 400


def test_obtener_rol_inexistente_devuelve_404(client):
    respuesta = client.get("/roles/999")
    assert respuesta.status_code == 404


def test_actualizar_y_eliminar_rol(client):
    rol = client.post("/roles/", json={"nombre_rol": "Auxiliar"}).json()
    actualizado = client.put(f"/roles/{rol['id_rol']}", json={"descripcion": "Apoyo administrativo"})
    assert actualizado.json()["descripcion"] == "Apoyo administrativo"
    eliminado = client.delete(f"/roles/{rol['id_rol']}")
    assert eliminado.status_code == 204
    assert client.get(f"/roles/{rol['id_rol']}").status_code == 404


def test_usuario_correo_duplicado(client):
    rol = client.post("/roles/", json={"nombre_rol": "Cajero"}).json()
    payload = {
        "nombre": "Luis",
        "correo": "luis@consultorio.ec",
        "id_rol": rol["id_rol"],
        "contrasena": "abc12345",
    }
    client.post("/usuarios/", json=payload)
    duplicado = client.post("/usuarios/", json=payload)
    assert duplicado.status_code == 400


def test_desactivar_y_eliminar_usuario(client):
    rol = client.post("/roles/", json={"nombre_rol": "Cajero2"}).json()
    usuario = client.post(
        "/usuarios/",
        json={
            "nombre": "Luis",
            "correo": "luis2@consultorio.ec",
            "id_rol": rol["id_rol"],
            "contrasena": "abc12345",
        },
    ).json()
    desactivado = client.patch(f"/usuarios/{usuario['id_usuario']}/desactivar")
    assert desactivado.json()["estado_activo"] is False
    eliminado = client.delete(f"/usuarios/{usuario['id_usuario']}")
    assert eliminado.status_code == 204


def test_buscar_pacientes(client):
    client.post("/pacientes/", json={"cedula_pasaporte": "1111111111", "nombre_completo": "Ana Torres"})
    resultado = client.get("/pacientes/buscar", params={"q": "Torres"})
    assert resultado.status_code == 200
    assert len(resultado.json()) == 1


def test_paciente_duplicado_devuelve_400(client):
    payload = {"cedula_pasaporte": "2222222222", "nombre_completo": "Pedro Ruiz"}
    client.post("/pacientes/", json=payload)
    duplicado = client.post("/pacientes/", json=payload)
    assert duplicado.status_code == 400


def test_actualizar_eliminar_paciente(client):
    paciente = client.post(
        "/pacientes/", json={"cedula_pasaporte": "3333333333", "nombre_completo": "Carla Vera"}
    ).json()
    actualizado = client.put(f"/pacientes/{paciente['id_paciente']}", json={"telefono": "0987654321"})
    assert actualizado.json()["telefono"] == "0987654321"
    eliminado = client.delete(f"/pacientes/{paciente['id_paciente']}")
    assert eliminado.status_code == 204


def test_buscar_medicos_por_especialidad(client):
    client.post(
        "/medicos/",
        json={
            "nombre_completo": "Dr. Juan Soto",
            "especialidad": "Cardiología",
            "registro_senescyt": "SEN-0099",
        },
    )
    resultado = client.get("/medicos/buscar", params={"especialidad": "Cardiología"})
    assert resultado.status_code == 200
    assert len(resultado.json()) == 1


def test_actualizar_eliminar_medico(client):
    medico = client.post(
        "/medicos/",
        json={
            "nombre_completo": "Dr. Iván Mora",
            "especialidad": "Dermatología",
            "registro_senescyt": "SEN-0100",
        },
    ).json()
    actualizado = client.put(
        f"/medicos/{medico['id_medico']}", json={"consultorio_asignado": "Consultorio 5"}
    )
    assert actualizado.json()["consultorio_asignado"] == "Consultorio 5"
    eliminado = client.delete(f"/medicos/{medico['id_medico']}")
    assert eliminado.status_code == 204


def test_agendar_cita_paciente_inexistente_devuelve_404(client):
    medico = client.post(
        "/medicos/",
        json={"nombre_completo": "Dr. X", "especialidad": "General", "registro_senescyt": "SEN-0200"},
    ).json()
    respuesta = client.post(
        "/citas/",
        json={
            "id_paciente": 999,
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-08-01T09:00:00",
        },
    )
    assert respuesta.status_code == 404


def test_obtener_cita_inexistente_devuelve_404(client):
    assert client.get("/citas/999").status_code == 404


def test_cancelar_cita_atendida_devuelve_400(client):
    paciente = client.post(
        "/pacientes/", json={"cedula_pasaporte": "4444444444", "nombre_completo": "Eva Soto"}
    ).json()
    medico = client.post(
        "/medicos/",
        json={"nombre_completo": "Dr. Z", "especialidad": "General", "registro_senescyt": "SEN-0300"},
    ).json()
    cita = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-08-02T09:00:00",
        },
    ).json()
    client.patch(f"/citas/{cita['id_cita']}/confirmar")
    client.patch(f"/citas/{cita['id_cita']}/iniciar-atencion")
    client.patch(f"/citas/{cita['id_cita']}/finalizar-atencion")
    respuesta = client.patch(f"/citas/{cita['id_cita']}/cancelar", json={"motivo_cancelacion": "x"})
    assert respuesta.status_code == 400


def test_registrar_consulta_sin_cita_en_atencion_devuelve_400(client):
    paciente = client.post(
        "/pacientes/", json={"cedula_pasaporte": "5555555555", "nombre_completo": "Mario Paz"}
    ).json()
    medico = client.post(
        "/medicos/",
        json={"nombre_completo": "Dr. W", "especialidad": "General", "registro_senescyt": "SEN-0400"},
    ).json()
    cita = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-08-03T09:00:00",
        },
    ).json()
    respuesta = client.post("/consultas/", json={"id_cita": cita["id_cita"]})
    assert respuesta.status_code == 400


def test_actualizar_consulta(client):
    paciente = client.post(
        "/pacientes/", json={"cedula_pasaporte": "6666666666", "nombre_completo": "Lucía Fuentes"}
    ).json()
    medico = client.post(
        "/medicos/",
        json={"nombre_completo": "Dra. Q", "especialidad": "General", "registro_senescyt": "SEN-0500"},
    ).json()
    cita = client.post(
        "/citas/",
        json={
            "id_paciente": paciente["id_paciente"],
            "id_medico": medico["id_medico"],
            "fecha_hora": "2026-08-04T09:00:00",
        },
    ).json()
    client.patch(f"/citas/{cita['id_cita']}/confirmar")
    client.patch(f"/citas/{cita['id_cita']}/iniciar-atencion")
    consulta = client.post("/consultas/", json={"id_cita": cita["id_cita"]}).json()
    actualizada = client.put(f"/consultas/{consulta['id_consulta']}", json={"diagnostico_cie10": "A09"})
    assert actualizada.json()["diagnostico_cie10"] == "A09"


def test_prescripcion_sin_consulta_devuelve_404(client):
    respuesta = client.post(
        "/prescripciones/",
        json={"id_consulta": 999, "medicamento": "Ibuprofeno", "dosis": "400mg", "frecuencia": "cada 12h"},
    )
    assert respuesta.status_code == 404


def test_orden_sin_consulta_devuelve_404(client):
    respuesta = client.post(
        "/ordenes-medicas/", json={"id_consulta": 999, "tipo": "Imagen", "descripcion": "Radiografía"}
    )
    assert respuesta.status_code == 404


def test_certificado_sin_consulta_devuelve_404(client):
    respuesta = client.post("/certificados/", json={"id_consulta": 999, "tipo": "salud"})
    assert respuesta.status_code == 404


def test_cuenta_contable_codigo_duplicado(client):
    payload = {"codigo": "5101", "nombre_cuenta": "Gastos varios", "tipo": "EGRESO"}
    client.post("/cuentas-contables/", json=payload)
    duplicado = client.post("/cuentas-contables/", json=payload)
    assert duplicado.status_code == 400


def test_comprobante_sin_consulta_devuelve_404(client):
    cuenta = client.post(
        "/cuentas-contables/", json={"codigo": "4102", "nombre_cuenta": "Otros ingresos", "tipo": "INGRESO"}
    ).json()
    respuesta = client.post(
        "/comprobantes/",
        json={"id_consulta": 999, "tipo": "factura", "total": 10.0, "id_cuenta_contable": cuenta["id_cuenta"]},
    )
    assert respuesta.status_code == 404


def test_consulta_publica_paciente_inexistente_devuelve_404(client):
    respuesta = client.get("/citas/publico/por-cedula/0000000000")
    assert respuesta.status_code == 404
