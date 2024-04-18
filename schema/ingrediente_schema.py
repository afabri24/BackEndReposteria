from pydantic import BaseModel
from typing import Optional

class IngredienteSchema(BaseModel):
    idIngrediente: Optional[int]
    nombre: str
    cantidad: float
    idMedida: int
    class Config:
        orm_mode = True