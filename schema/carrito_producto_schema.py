from pydantic import BaseModel
from typing import Optional

class CarritoProductoSchema(BaseModel):
    idCarrito:int
    idProducto:int