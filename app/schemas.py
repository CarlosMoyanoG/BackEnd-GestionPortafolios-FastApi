from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    mail: str
    rol: str
    prog_id: Optional[int] = None
    foto_url: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    mail: Optional[str] = None
    rol: Optional[str] = None
    prog_id: Optional[int] = None
    foto_url: Optional[str] = None

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
