from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    idUsuario: Optional[int]
    nombre: str
    apellido: str
    email: str
    password: str
    rol: int