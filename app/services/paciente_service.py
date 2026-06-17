from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.repositories.paciente_repository import PacienteRepository
from app.schemas.paciente import PacienteCreate, PacienteUpdate


class PacienteService:
    def __init__(self, db: Session):
        self.repo = PacienteRepository(db)

    def listar(self):
        return self.repo.list()

    def obtener(self, id_paciente: int) -> Paciente:
        paciente = self.repo.get(id_paciente)
        if not paciente:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Paciente no encontrado")
        return paciente

    def buscar(self, texto: str):
        return self.repo.buscar(texto)

    def crear(self, data: PacienteCreate) -> Paciente:
        if self.repo.get_by_cedula(data.cedula_pasaporte):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El paciente ya está registrado")
        return self.repo.create(Paciente(**data.model_dump()))

    def actualizar(self, id_paciente: int, data: PacienteUpdate) -> Paciente:
        paciente = self.obtener(id_paciente)
        return self.repo.update(paciente, data.model_dump(exclude_unset=True))

    def eliminar(self, id_paciente: int) -> None:
        self.repo.delete(self.obtener(id_paciente))
