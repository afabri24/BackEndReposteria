from sqlalchemy import Column, Integer, String, Table
from config.db import engine, meta_data

usuario = Table(
   'usuario', meta_data, 
   Column('idUsuario', Integer, primary_key=True, autoincrement=True),
   Column('nombre', String(50)),
   Column('apellido', String(50)),
   Column('email', String(255)),
   Column('password', String(32)),
   Column('rol', Integer)
)

meta_data.create_all(engine)


