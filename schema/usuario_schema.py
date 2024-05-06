from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    idUsuario: Optional[int]
    nombre: str
    apellido: str
    email: str
    password: str
    rol: int

class LoginSchema(BaseModel):
    email: str
    password: str

class ActualizarPerfilSchema(BaseModel):
    email: str
    nombre: Optional[str]
    apellido: Optional[str]
    password: Optional[str]

class ActualizarPerfilSchema(BaseModel):
    email_viejo: str
    nuevo_email: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None

class ActualizarContrasenaSchema(BaseModel):
    email: str
    password: str

class RegistrarUsuarioSchema(BaseModel):
    email: str
    password: str