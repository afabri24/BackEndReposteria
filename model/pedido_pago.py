from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float,LargeBinary
from config.db import engine, meta_data

pedido_pago = Table(
    'pedido_pago', meta_data,
    Column('idPago', Integer, primary_key=True),
    Column('idPedido', Integer, ForeignKey('pedido.idPedido')),
    Column('tipo', String(100)),
    Column('total', Float),
    Column('imagenPago64', LargeBinary)
)

meta_data.create_all(engine)
    