from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database, crud

router = APIRouter()

# Endpoint de cadastro de usuário
@router.post("/cadastro/", response_model=schemas.UsuarioOut)
def cadastrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Verifica se o e-mail já está cadastrado
    usuario_existente = db.query(crud.models.Usuario).filter(crud.models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    return crud.criar_usuario(db=db, usuario=usuario)
