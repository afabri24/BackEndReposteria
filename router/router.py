from fastapi import APIRouter
from schema.usuario_schema import UsuarioSchema
from model.usuario import usuario
from model.producto import producto
from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session


api_router = APIRouter()

@api_router.get("/")
def root():
    return {"message": "Hi, I'm the user router!"}


@api_router.get("/usuarios")
def obtener_todos_los_usuarios():
    with Session(engine) as session:
        stmt = select(usuario)
        result = session.execute(stmt)
        return [{"idUsuario": row.idUsuario, "nombre": row.nombre, "apellido": row.apellido, "email": row.email, "password": row.password, "rol": row.rol} for row in result]


@api_router.post("/usuario")
def crear_usuario(data_usuario:UsuarioSchema):
    new_usuario = data_usuario.dict()
    if 'id' in new_usuario:
        del new_usuario['id']
    with Session(engine) as session:
        session.execute(usuario.insert().values(**new_usuario))
        session.commit()
    return {"message": "Usuario creado correctamente"}
    

@api_router.put("/usuario/")
def actualizar_usuario(data_usuario:UsuarioSchema):
    print(data_usuario)

@api_router.get("/productos")
def obtener_todos_los_productos():
    with Session(engine) as session:
        stmt = select(producto)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, "nombre": row.nombre, "descripcion": row.descripcion, "costo": row.costo} for row in result]

    