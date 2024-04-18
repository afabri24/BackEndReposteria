from fastapi import APIRouter

# Importar los esquemas
from schema.usuario_schema import UsuarioSchema
from schema.producto_schema import ProductoSchema
from schema.producto_imagen_schema import ProductoImagenSchema
from schema.categoria_schema import CategoriaSchema
from schema.ingrediente_schema import IngredienteSchema
from schema.medida_schema import MedidaSchema
from schema.producto_categoria_schema import ProductoCategoriaSchema
from schema.producto_ingrediente_schema import ProductoIngredienteSchema

# Importar los modelos
from model.usuario import usuario
from model.producto import producto as Producto
from model.producto_imagen import producto_imagen
from model.categoria import categoria as Categoria
from model.ingrediente import ingrediente as Ingrediente
from model.producto_categoria import producto_categoria as ProductoCategoria
from model.producto_ingrediente import producto_ingrediente as ProductoIngrediente
from model.medida import medida as Medida


from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.orm import joinedload
from sqlalchemy import join
from sqlalchemy.sql import text


api_router = APIRouter()

@api_router.get("/")
def root():
    return {"message": "Hi, I'm the user router!"}

# Rutas de la API usuarios
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

# Rutas de la API productos
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
        result = session.execute(Producto.insert().values(**new_producto))
        session.commit()
        id_producto = result.inserted_primary_key[0]
    return {"message": "Producto creado correctamente", "idProducto": id_producto}

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

# Rutas de la API categorias
@api_router.get("/categorias")
def obtener_todas_las_categorias():
    with Session(engine) as session:
        stmt = select(Categoria)
        result = session.execute(stmt)
        return [{"idCategoria": row.idCategoria, "nombre": row.nombre} for row in result]
    

#
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



# Rutas de la API categoriaProducto
@api_router.get("/categoria_producto")
def obtener_todas_las_categorias_producto():
    with Session(engine) as session:
        stmt = select(ProductoCategoria.c.idProducto, Producto.c.nombre.label('nombreProducto'), Categoria.c.idCategoria, Categoria.c.nombre.label('nombreCategoria')).\
            join(Producto, Producto.c.idProducto == ProductoCategoria.c.idProducto).\
            join(Categoria, Categoria.c.idCategoria == ProductoCategoria.c.idCategoria)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, 
                 "nombreProducto": row.nombreProducto, 
                 "idCategoria": row.idCategoria, 
                 "nombreCategoria": row.nombreCategoria} for row in result]



@api_router.post("/categoria_producto")
def agregar_categoria_producto(id_producto:int, id_categoria:int):
    with Session(engine) as session:
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == id_producto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Verifica si la categoria existe
        categoria = session.query(Categoria).filter(Categoria.c.idCategoria == id_categoria).first()
        if not categoria:
            return {"error": "Categoria no encontrada"}
        # Inserta una nueva fila en la tabla ProductoCategoria
        session.execute(ProductoCategoria.insert().values(idProducto=id_producto, idCategoria=id_categoria))
        session.commit()
    return {"message": "Categoria producto creada correctamente"}


# Rutas de la API productoIngrediente
@api_router.get("/producto_ingrediente")
def obtener_todos_los_productos_ingredientes():
    with Session(engine) as session:
        stmt = select(ProductoIngrediente.c.idProducto, Producto.c.nombre.label('nombreProducto'), Ingrediente.c.idIngrediente, Ingrediente.c.nombre.label('nombreIngrediente'), Ingrediente.c.cantidad, Medida.c.tipo.label('nombreMedida')).\
            join(Producto, Producto.c.idProducto == ProductoIngrediente.c.idProducto).\
            join(Ingrediente, Ingrediente.c.idIngrediente == ProductoIngrediente.c.idIngrediente).\
            join(Medida, Medida.c.idMedida == Ingrediente.c.idMedida)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, 
                 "nombreProducto": row.nombreProducto, 
                 "idIngrediente": row.idIngrediente, 
                 "nombreIngrediente": row.nombreIngrediente, 
                 "cantidad": row.cantidad, 
                 "nombreMedida": row.nombreMedida} for row in result]
    
@api_router.post("/producto_ingrediente")
def agregar_producto_ingrediente(id_producto:int, id_ingrediente:int):
    with Session(engine) as session:
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == id_producto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Verifica si el ingrediente existe
        ingrediente = session.query(Ingrediente).filter(Ingrediente.c.idIngrediente == id_ingrediente).first()
        if not ingrediente:
            return {"error": "Ingrediente no encontrado"}
        # Inserta una nueva fila en la tabla ProductoIngrediente
        session.execute(ProductoIngrediente.insert().values(idProducto=id_producto, idIngrediente=id_ingrediente))
        session.commit()
    return {"message": "Producto ingrediente creado correctamente"}