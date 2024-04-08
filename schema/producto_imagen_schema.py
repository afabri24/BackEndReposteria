from pydantic import BaseModel
from typing import Optional

class ProductoImagenSchema(BaseModel):
    idProductoImagen: Optional[int]
    idProducto: int
    imagen64: str
    class Config:
        orm_mode = True