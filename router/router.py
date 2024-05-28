from fastapi import APIRouter, Response
from schema.usuario_schema import ActualizarPerfilSchema, LoginSchema, UsuarioSchema, ActualizarPerfilSchema, ActualizarContrasenaSchema, RegistrarUsuarioSchema
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
from schema.producto_categoria_schema import ProductoCategoriaSchema
from schema.producto_ingrediente_schema import ProductoIngredienteSchema
from schema.carrito_schema import CarritoSchema
from schema.direccion_schema import DireccionSchema
from schema.pedido_schema import PedidoSchema
from schema.pedido_producto_schema import PedidoProductoSchema
from schema.pedido_pago_schema import PedidoPagoSchema
from schema.carrito_producto_schema import CarritoProductoSchema
from schema.usuario_direccion_schema import UsuarioDireccionSchema



# Importar los modelos
from model.usuario import usuario
from model.producto import producto as Producto
from model.producto_imagen import producto_imagen
from model.categoria import categoria as Categoria
from model.ingrediente import ingrediente as Ingrediente
from model.producto_categoria import producto_categoria as ProductoCategoria
from model.producto_ingrediente import producto_ingrediente as ProductoIngrediente
from model.medida import medida as Medida
from model.carrito import carrito as Carrito
from model.direccion import direccion as Direccion
from model.pedido import pedido as Pedido
from model.pedido_producto import pedido_producto as PedidoProducto
from model.pedido_pago import pedido_pago as PedidoPago
from model.carrito_producto import carrito_producto as CarritoProducto
from model.usuario_direccion import usuario_direccion as UsuarioDireccion



from config.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import join
from sqlalchemy.sql import text
from sqlalchemy import select, join

from sqlalchemy import update

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
    
@api_router.get("/producto/{idProducto}")
def obtener_producto(idProducto:int):
    with Session(engine) as session:
        stmt = select(Producto).where(Producto.c.idProducto == idProducto)
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

@api_router.put("/producto")
def actualizar_producto(data_producto:ProductoSchema):
    new_producto = data_producto.dict()
    with Session(engine) as session:
        session.execute(Producto.update().where(Producto.c.idProducto == new_producto['idProducto']).values(nombre=new_producto['nombre'],descripcion=new_producto['descripcion'],costo=new_producto['costo']))
        session.commit()
    return {"message": "Producto actualizado correctamente"}

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
                        "email": usuario_db.email,
                        "idUsuario": usuario_db.idUsuario,
                        "rol": usuario_db.rol}
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
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
        
@api_router.get("/categoria_producto/{idProducto}")
def obtener_categorias_producto(idProducto:int):
    with Session(engine) as session:
        stmt = select(ProductoCategoria.c.idProducto, Producto.c.nombre.label('nombreProducto'), Categoria.c.idCategoria, Categoria.c.nombre.label('nombreCategoria')).\
            join(Producto, Producto.c.idProducto == ProductoCategoria.c.idProducto).\
            join(Categoria, Categoria.c.idCategoria == ProductoCategoria.c.idCategoria).\
            where(ProductoCategoria.c.idProducto == idProducto)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, 
                 "nombreProducto": row.nombreProducto, 
                 "idCategoria": row.idCategoria, 
                 "nombreCategoria": row.nombreCategoria} for row in result]



@api_router.post("/categoria_producto")
def agregar_categoria_producto(producto_categoria: ProductoCategoriaSchema):
    with Session(engine) as session:
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == producto_categoria.idProducto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Verifica si la categoria existe
        categoria = session.query(Categoria).filter(Categoria.c.idCategoria == producto_categoria.idCategoria).first()
        if not categoria:
            return {"error": "Categoria no encontrada"}
        # Inserta una nueva fila en la tabla ProductoCategoria
        session.execute(ProductoCategoria.insert().values(idProducto=producto_categoria.idProducto, idCategoria=producto_categoria.idCategoria))
        session.commit()
    return {"message": "Categoria producto creada correctamente"}

@api_router.delete("/categoria_producto")
def eliminar_categoria_producto(producto_categoria: ProductoCategoriaSchema):
    with Session(engine) as session:
        session.execute(ProductoCategoria.delete().where(ProductoCategoria.c.idProducto == producto_categoria.idProducto).where(ProductoCategoria.c.idCategoria == producto_categoria.idCategoria))
        session.commit()
    return {"message": "Categoria producto eliminada correctamente"}


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
        
@api_router.get("/producto_ingrediente/{idProducto}")
def obtener_ingredientes_producto(idProducto:int):
    with Session(engine) as session:
        stmt = select(ProductoIngrediente.c.idProducto, Producto.c.nombre.label('nombreProducto'), Ingrediente.c.idIngrediente, Ingrediente.c.nombre.label('nombreIngrediente'), Ingrediente.c.cantidad, Medida.c.tipo.label('nombreMedida')).\
            join(Producto, Producto.c.idProducto == ProductoIngrediente.c.idProducto).\
            join(Ingrediente, Ingrediente.c.idIngrediente == ProductoIngrediente.c.idIngrediente).\
            join(Medida, Medida.c.idMedida == Ingrediente.c.idMedida).\
            where(ProductoIngrediente.c.idProducto == idProducto)
        result = session.execute(stmt)
        return [{"idProducto": row.idProducto, 
                 "nombreProducto": row.nombreProducto, 
                 "idIngrediente": row.idIngrediente, 
                 "nombreIngrediente": row.nombreIngrediente, 
                 "cantidad": row.cantidad, 
                 "nombreMedida": row.nombreMedida} for row in result]
    
@api_router.post("/producto_ingrediente")
def agregar_producto_ingrediente(producto_ingrediente: ProductoIngredienteSchema):
    with Session(engine) as session:
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == producto_ingrediente.idProducto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Verifica si el ingrediente existe
        ingrediente = session.query(Ingrediente).filter(Ingrediente.c.idIngrediente == producto_ingrediente.idIngrediente).first()
        if not ingrediente:
            return {"error": "Ingrediente no encontrado"}
        # Inserta una nueva fila en la tabla ProductoIngrediente
        session.execute(ProductoIngrediente.insert().values(idProducto=producto_ingrediente.idProducto, idIngrediente=producto_ingrediente.idIngrediente))
        session.commit()
    return {"message": "Producto ingrediente creado correctamente"}

@api_router.delete("/producto_ingrediente")
def eliminar_producto_ingrediente(producto_ingrediente: ProductoIngredienteSchema):
    with Session(engine) as session:
        session.execute(ProductoIngrediente.delete().where(ProductoIngrediente.c.idProducto == producto_ingrediente.idProducto).where(ProductoIngrediente.c.idIngrediente == producto_ingrediente.idIngrediente))
        session.commit()
    return {"message": "Producto ingrediente eliminado correctamente"}

@api_router.get("/direccion/usuario/{idUsuario}")
def obtener_direccion_usuario(idUsuario:int):
    with Session(engine) as session:
        # Buscar en la tabla UsuarioDireccion
        usuario_direcciones = session.query(UsuarioDireccion).filter(UsuarioDireccion.c.idUsuario == idUsuario).all()
        if not usuario_direcciones:
            return {"error": "Usuario no encontrado"}

        # Buscar en la tabla Direccion
        direcciones = []
        for usuario_direccion in usuario_direcciones:
            stmt = select(Direccion).where(Direccion.c.idDireccion == usuario_direccion.idDireccion)
            result = session.execute(stmt)
            for row in result:
                direcciones.append({"idDireccion": row.idDireccion, "calle": row.calle, "ciudad": row.ciudad, "estado": row.estado,"colonia":row.colonia,"numeroExterior":row.numeroExterior,"numeroInterior":row.numeroInterior,"codigoPostal":row.codigoPostal})

        return direcciones
# Rutas de la API Direccion

@api_router.get("/direccion/{idDireccion}")
def obtener_direccion(idDireccion:int):
    with Session(engine) as session:
        stmt = select(Direccion).where(Direccion.c.idDireccion == idDireccion)
        result = session.execute(stmt)
        return [{"idDireccion": row.idDireccion, "calle": row.calle, "ciudad": row.ciudad, "estado": row.estado,"colonia":row.colonia,"numeroExterior":row.numeroExterior,"numeroInterior":row.numeroInterior,"codigoPostal":row.codigoPostal} for row in result]


    
@api_router.post("/direccion")
def crear_direccion(data_direccion:DireccionSchema):
    new_direccion = data_direccion.dict()
    if 'id' in new_direccion:
        del new_direccion['id']
    with Session(engine) as session:
        result = session.execute(Direccion.insert().values(**new_direccion))
        session.commit()
        idDireccion =result.inserted_primary_key[0]
    return {"message": "Direccion creada correctamente", "idDireccion": idDireccion}
        
@api_router.post("/direccionUsuario")
def agregar_direccion_usuario(usuario_direccion: UsuarioDireccionSchema):
    with Session(engine) as session:
        # Verifica si el usuario existe
        usuario = session.query(Usuario).filter(Usuario.c.idUsuario == usuario_direccion.idUsuario).first()
        if not usuario:
            return {"error": "Usuario no encontrado"}
        # Verifica si la direccion existe
        direccion = session.query(Direccion).filter(Direccion.c.idDireccion == usuario_direccion.idDireccion).first()
        if not direccion:
            return {"error": "Direccion no encontrada"}
        # Inserta una nueva fila en la tabla UsuarioDireccion
        session.execute(UsuarioDireccion.insert().values(idUsuario=usuario_direccion.idUsuario, idDireccion=usuario_direccion.idDireccion))
        session.commit()
    return {"message": "Direccion usuario creada correctamente"}

# Rutas de la API Carrito
from sqlalchemy import join

@api_router.get("/carrito/usuario/{idUsuario}")
def obtener_carrito_usuario(idUsuario:int):
    with Session(engine) as session:
        # Obtener el carrito del usuario
        stmt = select(Carrito).where(Carrito.c.idUsuario == idUsuario)
        result = session.execute(stmt)
        return [{"idCarrito": row.idCarrito, "idUsuario": row.idUsuario, "total": row.total} for row in result]

@api_router.post("/carrito")
def crear_carrito(data_carrito:CarritoSchema):
    new_carrito = data_carrito.dict()
    if 'id' in new_carrito:
        del new_carrito['id']
    with Session(engine) as session:
        session.execute(Carrito.insert().values(**new_carrito))
        session.commit()
    return {"message": "Carrito creado correctamente"}

@api_router.put("/carrito")
def actualizar_carrito(data_carrito:CarritoSchema):
    new_carrito = data_carrito.dict()
    with Session(engine) as session:
        session.execute(Carrito.update().where(Carrito.c.idCarrito == new_carrito['idCarrito']).values(idUsuario=new_carrito['idUsuario']))
        session.commit()
    return {"message": "Carrito actualizado correctamente"}



@api_router.post("/carrito_producto")
def agregar_producto_carrito(carrito_producto: CarritoProductoSchema):
    with Session(engine) as session:
        # Verifica si el carrito existe
        carrito = session.query(Carrito).filter(Carrito.c.idCarrito == carrito_producto.idCarrito).first()
        if not carrito:
            return {"error": "Carrito no encontrado"}
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == carrito_producto.idProducto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Inserta una nueva fila en la tabla CarritoProducto
        session.execute(CarritoProducto.insert().values(idCarrito=carrito_producto.idCarrito, idProducto=carrito_producto.idProducto))
        session.commit()
    return {"message": "Producto carrito creado correctamente"}

@api_router.get("/carrito_producto/{idCarrito}")
def obtener_productos_carrito(idCarrito:int):
    with Session(engine) as session:
        stmt = select(CarritoProducto.c.idCarrito, CarritoProducto.c.idProducto, Producto.c.nombre, Producto.c.costo).\
            join(Producto, Producto.c.idProducto == CarritoProducto.c.idProducto).\
            where(CarritoProducto.c.idCarrito == idCarrito)
        result = session.execute(stmt)
        return [{"idCarrito": row.idCarrito, "idProducto": row.idProducto, "nombre": row.nombre, "costo": row.costo} for row in result]

@api_router.delete("/carrito_producto")
def eliminar_producto_carrito(carrito_producto: CarritoProductoSchema):
    with Session(engine) as session:
        session.execute(CarritoProducto.delete().where(CarritoProducto.c.idCarrito == carrito_producto.idCarrito).where(CarritoProducto.c.idProducto == carrito_producto.idProducto))
        session.commit()
    return {"message": "Producto carrito eliminado correctamente"}

# Rutas de la API Pedido
@api_router.get("/pedidos")
def obtener_todos_los_pedidos():
    with Session(engine) as session:
        stmt = select(Pedido)
        result = session.execute(stmt)
        return [{"idPedido": row.idPedido, "fechaPedido": row.fechaPedido, "idUsuario": row.idUsuario, "idDireccion": row.idDireccion,"codigoPedido":row.codigoPedido,"fechaEntrega":row.fechaEntrega,"estado":row.estado} for row in result]
    
@api_router.get("/pedido/usuario/{idUsuario}")
def obtener_pedido_usuario(idUsuario:int):
    with Session(engine) as session:
        stmt = select(Pedido).where(Pedido.c.idUsuario == idUsuario)
        result = session.execute(stmt)
        return [{"idPedido": row.idPedido, "fechaPedido": row.fechaPedido, "idUsuario": row.idUsuario, "idDireccion": row.idDireccion,"codigoPedido":row.codigoPedido,"fechaEntrega":row.fechaEntrega,"estado":row.estado} for row in result]
    
@api_router.post("/pedido")
def crear_pedido(data_pedido:PedidoSchema):
    new_pedido = data_pedido.dict()
    if 'id' in new_pedido:
        del new_pedido['id']
    with Session(engine) as session:
        result = session.execute(Pedido.insert().values(**new_pedido))
        session.commit()
        idPedido = result.inserted_primary_key[0]
    return {"message": "Pedido creado correctamente", "idPedido": idPedido}

@api_router.put("/pedido")
def actualizar_pedido(data_pedido:PedidoSchema):
    new_pedido = data_pedido.dict()
    with Session(engine) as session:
        session.execute(Pedido.update().where(Pedido.c.idPedido == new_pedido['idPedido']).values(fechaPedido=new_pedido['fechaPedido'],idUsuario=new_pedido['idUsuario'],idDireccion=new_pedido['idDireccion'],codigoPedido=new_pedido['codigoPedido'],fechaEntrega=new_pedido['fechaEntrega'],estado=new_pedido['estado']))
        session.commit()
    return {"message": "Pedido actualizado correctamente"}

# Rutas de la API PedidoProducto
@api_router.get("/pedido_producto/{idPedido}")
def obtener_productos_pedido(idPedido:int):
    with Session(engine) as session:
        stmt = select(PedidoProducto.c.idPedido, PedidoProducto.c.idProducto, Producto.c.nombre, Producto.c.costo).\
            join(Producto, Producto.c.idProducto == PedidoProducto.c.idProducto).\
            where(PedidoProducto.c.idPedido == idPedido)
        result = session.execute(stmt)
        return [{"idPedido": row.idPedido, "idProducto": row.idProducto, "nombre": row.nombre, "costo": row.costo} for row in result]
    
@api_router.post("/pedido_producto")
def agregar_producto_pedido(pedido_producto: PedidoProductoSchema):
    with Session(engine) as session:
        # Verifica si el pedido existe
        pedido = session.query(Pedido).filter(Pedido.c.idPedido == pedido_producto.idPedido).first()
        if not pedido:
            return {"error": "Pedido no encontrado"}
        # Verifica si el producto existe
        producto = session.query(Producto).filter(Producto.c.idProducto == pedido_producto.idProducto).first()
        if not producto:
            return {"error": "Producto no encontrado"}
        # Inserta una nueva fila en la tabla PedidoProducto
        session.execute(PedidoProducto.insert().values(idPedido=pedido_producto.idPedido, idProducto=pedido_producto.idProducto))
        session.commit()
    return {"message": "Producto pedido creado correctamente"}

@api_router.delete("/pedido_producto")
def eliminar_producto_pedido(pedido_producto: PedidoProductoSchema):
    with Session(engine) as session:
        session.execute(PedidoProducto.delete().where(PedidoProducto.c.idPedido == pedido_producto.idPedido).where(PedidoProducto.c.idProducto == pedido_producto.idProducto))
        session.commit()
    return {"message": "Producto pedido eliminado correctamente"}

# Rutas de la API PedidoPago
@api_router.get("/pedido_pago/{idPedido}")
def obtener_pago_pedido(idPedido:int):
    with Session(engine) as session:
        stmt = select(PedidoPago).where(PedidoPago.c.idPedido == idPedido)
        result = session.execute(stmt)
        return [{"idPedido": row.idPedido, "idPago": row.idPago, "total": row.total, "tipo":row.tipo,"imagenPago64":row.imagenPago64} for row in result]
    
@api_router.post("/pedido_pago")
def agregar_pago_pedido(pedido_pago: PedidoPagoSchema):
    with Session(engine) as session:
        # Verifica si el pedido existe
        pedido = session.query(Pedido).filter(Pedido.c.idPedido == pedido_pago.idPedido).first()
        if not pedido:
            return {"error": "Pedido no encontrado"}
        # Inserta una nueva fila en la tabla PedidoPago
        session.execute(PedidoPago.insert().values(idPedido=pedido_pago.idPedido, total=pedido_pago.total, tipo=pedido_pago.tipo,imagenPago64=pedido_pago.imagenPago64))
        session.commit()
    return {"message": "Pago pedido creado correctamente"}

@api_router.put("/pedido_pago")
def actualizar_pago_pedido(pedido_pago: PedidoPagoSchema):
    with Session(engine) as session:
        session.execute(PedidoPago.update().where(PedidoPago.c.idPedido == pedido_pago.idPedido).where(PedidoPago.c.idPago == pedido_pago.idPago).values(total=pedido_pago.total, tipo=pedido_pago.tipo,imagenPago64=pedido_pago.imagenPago64))
        session.commit()
    return {"message": "Pago pedido actualizado correctamente"}

@api_router.delete("/pedido_pago")
def eliminar_pago_pedido(pedido_pago: PedidoPagoSchema):
    with Session(engine) as session:
        session.execute(PedidoPago.delete().where(PedidoPago.c.idPedido == pedido_pago.idPedido).where(PedidoPago.c.idPago == pedido_pago.idPago))
        session.commit()
    return {"message": "Pago pedido eliminado correctamente"}

# Rutas de la API

        
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
                values(email=usuario_data.email, password=usuario_data.password, rol=1)
            )
            session.execute(stmt)
            session.commit()
            return {"message": "Usuario registrado correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
@api_router.get("/productos_con_imagenes")
def obtener_productos_con_imagenes():
    with Session(engine) as session:
        # Realiza un JOIN entre las tablas Producto y producto_imagen
        stmt = select(Producto, producto_imagen.c.imagen64).\
            join(producto_imagen, Producto.c.idProducto == producto_imagen.c.idProducto)
        result = session.execute(stmt)
        
        # Formatea el resultado en un diccionario para cada producto con su información y sus imágenes
        productos_con_imagenes = [ 
            {
                "idProducto": row.idProducto,
                "nombre": row.nombre,
                "descripcion": row.descripcion,
                "costo": row.costo,
                "imagenes": [
                    {
                        "imagen64": row.imagen64
                    }
                ]
            } for row in result 
        ]
        
        return productos_con_imagenes




@api_router.get("/historialPedidos/{email}")
def obtener_historial_pedidos(email: str):
    with Session(engine) as session:
        try:
            usuario = session.query(Usuario).filter(Usuario.c.email == email).one()
            stmt = (
                select(
                    Pedido.c.codigoPedido,
                    Pedido.c.estado,
                    Pedido.c.fechaPedido,
                    Pedido.c.fechaEntrega,
                    Direccion.c.calle,
                    Direccion.c.colonia
                ).
                select_from(
                    Pedido.join(Usuario, Usuario.c.idUsuario == Pedido.c.idUsuario).
                    join(Direccion, Direccion.c.idDireccion == Pedido.c.idDireccion)
                )
            )
            if usuario.rol != 2:
                stmt = stmt.where(Usuario.c.email == email)
            else:
                stmt = stmt.add_columns(Usuario.c.nombre)
            result = session.execute(stmt).fetchall()
            return [
                {
                    "codigoPedido": row.codigoPedido,
                    "estado": row.estado,
                    "fechaPedido": row.fechaPedido,
                    "fechaEntrega": row.fechaEntrega,
                    "calle": row.calle,
                    "colonia": row.colonia,
                    "nombreUsuario": row.nombre if usuario.rol == 2 else None
                } for row in result
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))