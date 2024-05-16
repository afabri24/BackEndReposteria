from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

producto_ingrediente = Table(
    'producto_ingrediente', meta_data,
    Column('idProducto', Integer, ForeignKey('producto.idProducto')),
    Column('idIngrediente', Integer, ForeignKey('ingrediente.idIngrediente'))
)

meta_data.create_all(engine)