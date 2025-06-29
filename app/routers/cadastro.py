from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from app.utils.security import hash_password

router = APIRouter(prefix="/cadastro", tags=["Cadastro"])

@router.post("/")
def cadastrar_usuario(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    genero: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = User(nome=nome, email=email, senha=hash_password(senha), genero=genero)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"status": "ok", "id": usuario.id, "email": usuario.email}
