from pydantic import BaseModel
from typing import Optional

class UsuarioDireccionSchema(BaseModel):
    idDireccion: int
    idUsuario: int
    
    