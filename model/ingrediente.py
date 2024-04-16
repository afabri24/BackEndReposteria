from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.db import engine, meta_data

ingrediente = Table(
    'ingrediente', meta_data, 
    Column('idIngrediente', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50)),
    Column('cantidad', Integer),
    Column('idMedida', Integer, ForeignKey('medida.idMedida'))


)

meta_data.create_all(engine)