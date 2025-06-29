from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.database import engine, SessionLocal
from app.models import Base, Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioOut, UsuarioLogin
from app.utils.auth import pwd_context, criar_token, verificar_token
from pagamento import router as pagamento_router  # ✅ IMPORTADO

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(
    title="API Coelhas",
    version="1.0.0",
    description="Backend oficial do site Coelhas.com.br",
)

# CORS liberado para o frontend oficial
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://coelhas.com.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sessão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de teste
@app.get("/")
def home():
    return {"mensagem": "API Coelhas.com.br online em modo produção ✅"}

# Rota de cadastro de usuários
@app.post("/cadastro/", response_model=UsuarioOut)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=pwd_context.hash(usuario.senha),
        genero=usuario.genero,
        is_admin=usuario.is_admin or False
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# Rota de login
@app.post("/login/")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not user or not pwd_context.verify(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": user.email})
    return {
        "token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }

# Listar todos os usuários (protegido)
@app.get("/usuarios/", response_model=list[UsuarioOut])
def listar(db: Session = Depends(get_db), usuario_logado: Usuario = Depends(verificar_token)):
    return db.query(Usuario).all()

# Editar usuário
@app.put("/usuarios/{id}/", response_model=UsuarioOut)
def editar(id: int, dados: UsuarioCreate, db: Session = Depends(get_db), usuario_logado: Usuario = Depends(verificar_token)):
    user = db.query(Usuario).get(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.nome = dados.nome
    user.email = dados.email
    user.senha = pwd_context.hash(dados.senha)
    user.genero = dados.genero
    user.is_admin = dados.is_admin or False
    db.commit()
    db.refresh(user)
    return user

# Deletar usuário
@app.delete("/usuarios/{id}/")
def deletar(id: int, db: Session = Depends(get_db), usuario_logado: Usuario = Depends(verificar_token)):
    user = db.query(Usuario).get(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}

# ✅ Incluindo o router de pagamento Mercado Pago
app.include_router(pagamento_router)
