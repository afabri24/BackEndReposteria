from pydantic import BaseModel
from typing import Optional


class CarritoSchema(BaseModel):
    idCarrito: Optional[int]
    idUsuario: int
    total: float