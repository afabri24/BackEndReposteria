from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float
from config.db import engine, meta_data

carrito = Table(
    'carrito', meta_data,
    Column('idCarrito', Integer, primary_key=True),
    Column('idUsuario', Integer, ForeignKey('usuario.idUsuario')),
    Column('total', Float)
)