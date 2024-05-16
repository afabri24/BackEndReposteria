from sqlalchemy import Column, Integer, String, Table
from config.db import engine, meta_data

medida = Table(
    'medida', meta_data, 
    Column('idMedida', Integer, primary_key=True, autoincrement=True),
    Column('tipo', String(30))
)

meta_data.create_all(engine)