from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

producto_categoria = Table(
    'producto_categoria', meta_data,
    Column('idProducto', Integer, ForeignKey('producto.idProducto')),
    Column('idCategoria', Integer, ForeignKey('categoria.idCategoria'))
)

meta_data.create_all(engine)