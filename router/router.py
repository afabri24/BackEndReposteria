from fastapi import APIRouter
from schema.usuario_schema import UsuarioSchema
from model.usuario import usuario
from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session


usuario_router = APIRouter()

@usuario_router.get("/")
def root():
    return {"message": "Hi, I'm the user router!"}


@usuario_router.get("/usuario")
def obtener_todos_los_usuarios():
    conn = engine.connect()
    query = usuario.select()
    result = conn.execute(query).fetchall()
    return [dict(row) for row in result]

# @usuario_router.get("/usuario/{usuario_id}")
# def obtener_usuario(usuario_id:int):
#     query = usuario.select().where(usuario.c.idUsuario == usuario_id)
#     return conn.execute(query).fetchone()

# @usuario_router.post("/usuario")
# def crear_usuario(data_usuario:UsuarioSchema):
#     new_usuario = data_usuario.dict()
#     if 'id' in new_usuario:
#         del new_usuario['id']
#     conn.execute(usuario.insert().values(new_usuario))
#     return {"message": "Usuario creado correctamente"}
    

@usuario_router.put("/usuario/")
def actualizar_usuario(data_usuario:UsuarioSchema):
    print(data_usuario)
    