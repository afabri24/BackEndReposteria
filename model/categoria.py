from sqlalchemy import Column, Integer, String, Table
from config.db import engine, meta_data

categoria = Table(
    'categoria', meta_data,
    Column('idCategoria', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50))
)

meta_data.create_all(engine)