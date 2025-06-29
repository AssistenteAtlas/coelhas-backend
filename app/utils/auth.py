from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import Usuario  # ✅ import corrigido

# Configurações de produção do JWT
SECRET_KEY = "coelhas-secret-key"  # Em produção, use variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Middleware OAuth2 (usa Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Gerador de hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar token JWT
def criar_token(dados: dict):
    dados_copy = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copy.update({"exp": expire})
    return jwt.encode(dados_copy, SECRET_KEY, algorithm=ALGORITHM)

# Verifica token e retorna o usuário logado
def verificar_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise cred_exception
    except JWTError:
        raise cred_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise cred_exception
    return usuario
