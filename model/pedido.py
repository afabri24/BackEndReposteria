from sqlalchemy import Column, Integer, String, Table, ForeignKey,Date, DateTime
from config.db import engine, meta_data

pedido = Table(
    'pedido', meta_data,
    Column('idPedido', Integer, primary_key=True),
    Column('codigoPedido', String(100)),
    Column('idUsuario', Integer, ForeignKey('usuario.idUsuario')),
    Column('idDireccion', Integer, ForeignKey('direccion.idDireccion')),
    Column('fechaPedido', Date),
    Column('fechaEntrega', DateTime),
    Column('estado', String(100)),
)

meta_data.create_all(engine)