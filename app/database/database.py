from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Conexão com o banco (ex: postgresql://usuario:senha@localhost:5432/nomedb)
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o engine (conector com o banco)
engine = create_engine(DATABASE_URL)

# Cria a sessão (para fazer queries e commits)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models
Base = declarative_base()

# Função para obter a sessão do banco (usada nos endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
