from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    id: Optional[int]
    nombre: str
    apellido: str
    email: str
    password: str
    rol: int