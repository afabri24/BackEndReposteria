from pydantic import BaseModel
from typing import Optional

class ProductoImagenSchema(BaseModel):
    idProductoImagen: Optional[int]
    idProducto: int
    imagen64: bytes
    class Config:
        orm_mode = True