from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PedidoSchema(BaseModel):
    idPedido: Optional[int]
    idDireccion: int
    idUsuario: int
    fechaPedido: date
    fechaEntrega: datetime
    estado: str
    codigoPedido: str
    
class PedidoEstadoSchema(BaseModel):
    idPedido: int
    estado: str
    