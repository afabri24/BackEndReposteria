from pydantic import BaseModel
from typing import Optional

class ProductoSchema(BaseModel):
    idProducto: Optional[int]
    nombre: str
    descripcion: str
    costo: float
