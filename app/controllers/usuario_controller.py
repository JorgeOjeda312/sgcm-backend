from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Configuración - Usuarios"])


@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).listar()


@router.get("/{id_usuario}", response_model=UsuarioOut)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return UsuarioService(db).obtener(id_usuario)


@router.post("/", response_model=UsuarioOut, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService(db).crear(data)


@router.put("/{id_usuario}", response_model=UsuarioOut)
def actualizar_usuario(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    return UsuarioService(db).actualizar(id_usuario, data)


@router.patch("/{id_usuario}/desactivar", response_model=UsuarioOut)
def desactivar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return UsuarioService(db).desactivar(id_usuario)


@router.delete("/{id_usuario}", status_code=204)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    UsuarioService(db).eliminar(id_usuario)
