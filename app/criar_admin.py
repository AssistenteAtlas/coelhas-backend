import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.database import SessionLocal
from app.models import Usuario  # ❌ ERRO! Aqui está o problema — models.py não é um módulo

# ✅ CORRETO:
from app import models
from app.utils.auth import pwd_context

# Cria sessão
db = SessionLocal()

# Verifica se já existe
admin_email = "nertech@admin.com"
if db.query(models.Usuario).filter(models.Usuario.email == admin_email).first():
    print("Admin já existe.")
else:
    novo = models.Usuario(
        nome="Administrador",
        email=admin_email,
        senha=pwd_context.hash("Nertech2025@"),
        genero="Outro",
        is_admin=True
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    print("Admin criado com sucesso ✅")
