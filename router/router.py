from fastapi import APIRouter, Response
from schema.usuario_schema import LoginSchema, UsuarioSchema
from schema.producto_schema import ProductoSchema
from schema.producto_imagen_schema import ProductoImagenSchema
from model.usuario import usuario as Usuario
from fastapi import APIRouter

# Importar los esquemas
from schema.usuario_schema import UsuarioSchema
from schema.producto_schema import ProductoSchema
from schema.producto_imagen_schema import ProductoImagenSchema
from schema.categoria_schema import CategoriaSchema
from schema.ingrediente_schema import IngredienteSchema
from schema.medida_schema import MedidaSchema

# Importar los modelos
from model.usuario import usuario
from model.producto import producto as Producto
from model.producto_imagen import producto_imagen
from model.categoria import categoria as Categoria
from model.ingrediente import ingrediente as Ingrediente
from model.medida import medida as Medida


from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import join
from sqlalchemy.sql import text


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
                return {"message": "Inicio de sesión exitoso"}
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
@api_router.get("/categorias")
def obtener_todas_las_categorias():
    with Session(engine) as session:
        stmt = select(Categoria)
        result = session.execute(stmt)
        return [{"idCategoria": row.idCategoria, "nombre": row.nombre} for row in result]


@api_router.get("/ingredientes")
def obtener_todos_los_ingredientes():
    with Session(engine) as session:
        stmt = text("SELECT ingrediente.`idIngrediente`, ingrediente.nombre, ingrediente.cantidad, ingrediente.`idMedida`, medida.tipo FROM ingrediente INNER JOIN medida ON ingrediente.`idMedida` = medida.`idMedida`")
        # stmt = select(Ingrediente.c.idIngrediente, Ingrediente.c.nombre, Ingrediente.c.cantidad, Ingrediente.c.idMedida, Medida.c.tipo).select_from(Ingrediente.join(Medida, Ingrediente.c.idMedida == Medida.c.idMedida))
        result = session.execute(stmt)
        return [{"idIngrediente": row.idIngrediente, "nombre": row.nombre, "cantidad": row.cantidad, "idMedida": row.idMedida, "nombreMedida": row.tipo} for row in result]
    
@api_router.post("/ingrediente")
def crear_ingrediente(data_ingrediente:IngredienteSchema):
    new_ingrediente = data_ingrediente.dict()
    if 'id' in new_ingrediente:
        del new_ingrediente['id']
    with Session(engine) as session:
        session.execute(Ingrediente.insert().values(**new_ingrediente))
        session.commit()
    return {"message": "Ingrediente creado correctamente"}

    
    
