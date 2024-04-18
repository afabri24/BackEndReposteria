from pydantic import BaseModel
from typing import Optional

class ProductoCategoriaSchema(BaseModel):
    idProducto: int
    idCategoria: int
    class Config:
        orm_mode = True