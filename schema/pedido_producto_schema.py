from pydantic import BaseModel
from typing import Optional

class PedidoProductoSchema(BaseModel):
    idPedido: int
    idProducto: int