"""
Pruebas unitarias de UsuarioService (RF-C01, RNF-04).

Se utiliza unittest.mock.Mock para sustituir el repositorio por un doble
de prueba, de forma que UsuarioService se valida de forma aislada, sin
depender de SQLAlchemy ni de una base de datos real (patrón equivalente
al uso de Mockito en Java).
"""
import unittest
from unittest.mock import Mock

from fastapi import HTTPException

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.usuario_service import UsuarioService, _hash_password


class TestHashPassword(unittest.TestCase):
    """RNF-04: las contraseñas nunca se almacenan en texto plano."""

    def test_hash_es_determinista(self):
        self.assertEqual(_hash_password("abc123"), _hash_password("abc123"))

    def test_hash_distinto_para_claves_distintas(self):
        self.assertNotEqual(_hash_password("abc123"), _hash_password("xyz789"))

    def test_hash_no_es_igual_al_texto_plano(self):
        self.assertNotEqual(_hash_password("abc123"), "abc123")


class TestUsuarioService(unittest.TestCase):
    def setUp(self):
        self.service = UsuarioService(Mock())
        self.service.repo = Mock()

    def test_listar_delega_en_el_repositorio(self):
        self.service.repo.list.return_value = ["u1", "u2"]
        self.assertEqual(self.service.listar(), ["u1", "u2"])
        self.service.repo.list.assert_called_once()

    def test_obtener_usuario_existente(self):
        usuario = Usuario(id_usuario=1, nombre="Ana")
        self.service.repo.get.return_value = usuario
        self.assertIs(self.service.obtener(1), usuario)

    def test_obtener_usuario_inexistente_lanza_404(self):
        self.service.repo.get.return_value = None
        with self.assertRaises(HTTPException) as ctx:
            self.service.obtener(99)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_crear_usuario_correo_duplicado_lanza_400(self):
        self.service.repo.get_by_correo.return_value = Usuario(id_usuario=1)
        data = UsuarioCreate(nombre="Ana", correo="ana@ups.edu.ec", id_rol=1, contrasena="abc123")
        with self.assertRaises(HTTPException) as ctx:
            self.service.crear(data)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_crear_usuario_hashea_la_contrasena(self):
        self.service.repo.get_by_correo.return_value = None
        self.service.repo.create.side_effect = lambda obj: obj
        data = UsuarioCreate(nombre="Ana", correo="ana@ups.edu.ec", id_rol=1, contrasena="abc123")
        usuario = self.service.crear(data)
        self.assertEqual(usuario.contrasena_hash, _hash_password("abc123"))
        self.assertNotEqual(usuario.contrasena_hash, "abc123")

    def test_actualizar_usuario(self):
        usuario = Usuario(id_usuario=1, nombre="Ana")
        self.service.repo.get.return_value = usuario
        self.service.repo.update.return_value = usuario
        data = UsuarioUpdate(nombre="Ana María")
        self.service.actualizar(1, data)
        self.service.repo.update.assert_called_once_with(usuario, {"nombre": "Ana María"})

    def test_desactivar_usuario(self):
        usuario = Usuario(id_usuario=1, estado_activo=True)
        self.service.repo.get.return_value = usuario
        self.service.repo.update.return_value = usuario
        self.service.desactivar(1)
        self.service.repo.update.assert_called_once_with(usuario, {"estado_activo": False})

    def test_eliminar_usuario(self):
        usuario = Usuario(id_usuario=1)
        self.service.repo.get.return_value = usuario
        self.service.eliminar(1)
        self.service.repo.delete.assert_called_once_with(usuario)


if __name__ == "__main__":
    unittest.main()
