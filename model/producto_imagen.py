from sqlalchemy import Column, Integer, String, Table,BLOB,ForeignKey
from config.db import engine, meta_data


producto_imagen = Table(
    'producto_imagen', meta_data,
    Column('idProductoImagen', Integer, primary_key=True, autoincrement=True),
    Column('imagen64', BLOB),
    Column('idProducto', Integer, ForeignKey('producto.idProducto'))
)

meta_data.create_all(engine)