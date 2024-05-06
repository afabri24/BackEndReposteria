from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

direccion = Table(
    'direccion', meta_data,
    Column('idDireccion', Integer, primary_key=True),
    Column('calle', String(100)),
    Column('numeroExterior', Integer),
    Column('numeroInterior', Integer),
    Column('colonia', String(100)),
    Column('codigoPostal', String(8)),
    Column('ciudad', String(100)),
    Column('estado', String(100)),
)