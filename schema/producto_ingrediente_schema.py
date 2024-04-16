from pydantic import BaseModel
from typing import Optional

class ProductoIngredienteSchema(BaseModel):
    idProducto:int
    idIngrediente:int
    class Config:
        orm_mode = True