import hashlib
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def _hash_password(password: str) -> str:
    """RNF-04: las contraseñas nunca se guardan en texto plano.

    Devuelve el hash SHA-256 de ``password`` en formato hexadecimal.

    >>> _hash_password("clave123") == _hash_password("clave123")
    True
    >>> len(_hash_password("clave123"))
    64
    >>> _hash_password("clave123") == "clave123"
    False

    Nota académica: se usa sha256 con fines demostrativos; en un entorno
    productivo se debe usar bcrypt (factor de coste >= 12) tal como exige
    la SRS (RNF-04).
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_usuario: int) -> Usuario:
        usuario = self.repo.get(id_usuario)
        if not usuario:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
        return usuario

    def crear(self, data: UsuarioCreate) -> Usuario:
        if self.repo.get_by_correo(data.correo):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El correo ya está registrado")
        payload = data.model_dump(exclude={"contrasena"})
        usuario = Usuario(**payload, contrasena_hash=_hash_password(data.contrasena))
        return self.repo.create(usuario)

    def actualizar(self, id_usuario: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.obtener(id_usuario)
        return self.repo.update(usuario, data.model_dump(exclude_unset=True))

    def desactivar(self, id_usuario: int) -> Usuario:
        usuario = self.obtener(id_usuario)
        return self.repo.update(usuario, {"estado_activo": False})

    def eliminar(self, id_usuario: int) -> None:
        self.repo.delete(self.obtener(id_usuario))
