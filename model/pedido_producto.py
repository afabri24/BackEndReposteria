from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

pedido_producto = Table(
    'pedido_producto', meta_data,
    Column('idPedido', Integer, ForeignKey('pedido.idPedido')),
    Column('idProducto', Integer, ForeignKey('producto.idProducto'))
)

meta_data.create_all(engine)