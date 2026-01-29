from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, service

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Usuarios API - FastAPI")

def get_usuario_service(db: Session = Depends(database.get_db)):
    return service.UsuarioService(db)

@app.get("/api/usuarios", response_model=List[schemas.Usuario])
def read_usuarios(service: service.UsuarioService = Depends(get_usuario_service)):
    return service.get_all()

@app.get("/api/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, service: service.UsuarioService = Depends(get_usuario_service)):
    usuario = service.get_by_id(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/api/usuarios", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: schemas.UsuarioCreate, service: service.UsuarioService = Depends(get_usuario_service)):
    return service.create(usuario)

@app.put("/api/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, service: service.UsuarioService = Depends(get_usuario_service)):
    db_usuario = service.update(usuario_id, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.delete("/api/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, service: service.UsuarioService = Depends(get_usuario_service)):
    if not service.delete(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
