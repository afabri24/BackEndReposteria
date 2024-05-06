from pydantic import BaseModel
from typing import Optional

class DireccionSchema(BaseModel):
    idDireccion: Optional[int]
    calle: str
    numeroExterior: int
    numeroInterior: Optional[int]
    colonia: str
    codigoPostal: str
    ciudad: str
    estado: str