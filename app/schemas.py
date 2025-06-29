from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema para criação de usuário (entrada da API)
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    genero: Optional[str] = None
    is_admin: Optional[bool] = False  # Novo campo opcional

# Schema de retorno (saída da API), com ID
class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    genero: Optional[str] = None
    is_admin: bool  # Retorna se é admin

    class Config:
        orm_mode = True
