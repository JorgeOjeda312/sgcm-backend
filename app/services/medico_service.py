from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.repositories.medico_repository import MedicoRepository
from app.schemas.medico import MedicoCreate, MedicoUpdate


class MedicoService:
    def __init__(self, db: Session):
        self.repo = MedicoRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_medico: int) -> Medico:
        medico = self.repo.get(id_medico)
        if not medico:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Médico no encontrado")
        return medico

    def buscar(self, texto: str | None, especialidad: str | None):
        return self.repo.buscar(texto, especialidad)

    def crear(self, data: MedicoCreate) -> Medico:
        return self.repo.create(Medico(**data.model_dump()))

    def actualizar(self, id_medico: int, data: MedicoUpdate) -> Medico:
        medico = self.obtener(id_medico)
        return self.repo.update(medico, data.model_dump(exclude_unset=True))

    def eliminar(self, id_medico: int) -> None:
        self.repo.delete(self.obtener(id_medico))
