from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

usuario_direccion = Table(
    'usuario_direccion', meta_data,
    Column('idUsuario', Integer, ForeignKey('usuario.idUsuario')),
    Column('idDireccion', Integer, ForeignKey('direccion.idDireccion'))
)

meta_data.create_all(engine)