from sqlalchemy import Column, Integer, String, Table,Float
from config.db import engine, meta_data

producto = Table(
    'producto', meta_data, 
    Column('idProducto', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50)),
    Column('descripcion', String(255)),
    Column('costo', Float)
)

meta_data.create_all(engine)