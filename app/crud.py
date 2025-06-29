from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

# Criptografar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar hash da senha
def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

# Função para criar usuário
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        genero=usuario.genero
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
