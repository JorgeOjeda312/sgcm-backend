from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.rol_service import RolService
from app.schemas.rol import RolCreate, RolUpdate, RolOut

router = APIRouter(prefix="/roles", tags=["Configuración - Roles"])


@router.get("/", response_model=list[RolOut])
def listar_roles(db: Session = Depends(get_db)):
    return RolService(db).listar()


@router.get("/{id_rol}", response_model=RolOut)
def obtener_rol(id_rol: int, db: Session = Depends(get_db)):
    return RolService(db).obtener(id_rol)


@router.post("/", response_model=RolOut, status_code=201)
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return RolService(db).crear(data)


@router.put("/{id_rol}", response_model=RolOut)
def actualizar_rol(id_rol: int, data: RolUpdate, db: Session = Depends(get_db)):
    return RolService(db).actualizar(id_rol, data)


@router.delete("/{id_rol}", status_code=204)
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    RolService(db).eliminar(id_rol)
