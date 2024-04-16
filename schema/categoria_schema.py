from pydantic import BaseModel
from typing import Optional

class CategoriaSchema(BaseModel):
    idCategoria: Optional[int]
    nombre: str
    class Config:
        orm_mode = True