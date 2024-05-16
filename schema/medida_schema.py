from pydantic import BaseModel
from typing import Optional

class MedidaSchema(BaseModel):
    idMedida: Optional[int]
    nombre: str
    class Config:
        orm_mode = True