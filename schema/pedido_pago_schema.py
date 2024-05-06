from pydantic import BaseModel
from typing import Optional

class PedidoPagoSchema(BaseModel):
    idPago: Optional[int]
    idPedido: int
    total: float
    tipo: str
    imagenPago64: Optional[bytes]
    class Config:
        orm_mode = True