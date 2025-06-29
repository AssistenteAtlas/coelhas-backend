from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base  # ✅ Corrigido aqui

class Usuario(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha = Column(String, nullable=False)
    genero = Column(String)
    is_admin = Column(Boolean, default=False)  # 👈 campo que define se é admin
