from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

carrito_producto = Table(
    'carrito_producto', meta_data,
    Column('idCarrito', Integer, ForeignKey('carrito.idCarrito')),
    Column('idProducto', Integer, ForeignKey('producto.idProducto'))
)