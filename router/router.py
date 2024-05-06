from fastapi import APIRouter, Response
from schema.usuario_schema import ActualizarPerfilSchema, LoginSchema, UsuarioSchema, ActualizarPerfilSchema, ActualizarContrasenaSchema, RegistrarUsuarioSchema
from schema.producto_schema import ProductoSchema
from schema.producto_imagen_schema import ProductoImagenSchema
from model.usuario import usuario as Usuario
from model.producto import producto as Producto
from model.producto_imagen import producto_imagen
from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

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
        stmt = select(Producto)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, "nombre": row.nombre, "descripcion": row.descripcion, "costo": row.costo} for row in result]
    
@api_router.post("/productos")
def crear_producto(data_producto:ProductoSchema):
    new_producto = data_producto.dict()
    if 'id' in new_producto:
        del new_producto['id']
    with Session(engine) as session:
        session.execute(Producto.insert().values(**new_producto))
        session.commit()
    return {"message": "Producto creado correctamente"}

@api_router.post("/imagen_producto")
def crear_imagen_producto(data_producto_imagen:ProductoImagenSchema):
    new_producto_imagen = data_producto_imagen.dict()
    if 'id' in new_producto_imagen:
        del new_producto_imagen['id']
    with Session(engine) as session:
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == new_producto_imagen['idProducto']).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Inserta la imagen del producto
        session.execute(producto_imagen.insert().values(**new_producto_imagen))
        session.commit()
    return {"message": "Imagen producto creada correctamente"}


@api_router.post("/login")
def login(usuario: LoginSchema):
    with Session(engine) as session:
        try:
            usuario_db = session.query(Usuario).filter(Usuario.c.email == usuario.email).one()
            if usuario_db.password == usuario.password:
                return {"message": "Inicio de sesión exitoso",
                        "email": usuario_db.email}
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        

        
@api_router.get("/editarPerfil/{email}")
def obtener_perfil(email: str):
    with Session(engine) as session:
        try:
            usuario_db = session.query(Usuario).filter(Usuario.c.email == email).one()
            return {
                "nombre": usuario_db.nombre,
                "apellido": usuario_db.apellido,
                "email": usuario_db.email,
            }
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        

@api_router.put("/editarPerfil")
def actualizar_perfil(usuario_data: ActualizarPerfilSchema):
    with Session(engine) as session:
        try:
            stmt = (
                update(Usuario).
                where(Usuario.c.email == usuario_data.email_viejo)
            )
            if usuario_data.nombre is not None:
                stmt = stmt.values(nombre=usuario_data.nombre)
            if usuario_data.apellido is not None:
                stmt = stmt.values(apellido=usuario_data.apellido)
            if usuario_data.nuevo_email is not None:
                stmt = stmt.values(email=usuario_data.nuevo_email)
            result = session.execute(stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            session.commit()
            return {"message": "Perfil actualizado correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
@api_router.put("/cambiarContrasena")
def cambiar_contrasena(usuario_data: ActualizarContrasenaSchema):
    with Session(engine) as session:
        try:
            stmt = (
                update(Usuario).
                where(Usuario.c.email == usuario_data.email).
                values(password=usuario_data.password)
            )
            result = session.execute(stmt)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            session.commit()
            return {"message": "Contraseña actualizada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

@api_router.post("/registrarUsuario")
def registrar_usuario(usuario_data: RegistrarUsuarioSchema):
    with Session(engine) as session:
        try:
            stmt = (
                insert(Usuario).
                values(email=usuario_data.email, password=usuario_data.password)
            )
            session.execute(stmt)
            session.commit()
            return {"message": "Usuario registrado correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))