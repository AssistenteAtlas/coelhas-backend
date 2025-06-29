import mercadopago
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# SDK do Mercado Pago
sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_TOKEN"))

# Modelo de dados do pagamento
class DadosPagamento(BaseModel):
    titulo: str
    valor: float

# Endpoint para gerar link de pagamento
@router.post("/api/pagamento")
def gerar_link_pagamento(dados: DadosPagamento):
    try:
        preference_data = {
            "items": [
                {
                    "title": dados.titulo,
                    "quantity": 1,
                    "unit_price": dados.valor,
                    "currency_id": "BRL"
                }
            ],
            "back_urls": {
                "success": "https://coelhas.com.br/pagamento-sucesso.html",
                "failure": "https://coelhas.com.br/pagamento-falhou.html",
                "pending": "https://coelhas.com.br/pagamento-pendente.html"
            },
            "auto_return": "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        return {"link_pagamento": preference_response["response"]["init_point"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar pagamento: {str(e)}")

# Endpoint do Webhook para confirmação automática
@router.post("/webhook")
async def mercado_pago_webhook(request: Request):
    try:
        # Assinatura secreta configurada no Mercado Pago
        segredo = b"1072f8f4131bdb100f9d8b42a44968a63ec6d2ce18d63f169d5ec2d63ce1d5c"
        assinatura_recebida = request.headers.get("x-signature")

        # Verificação da assinatura HMAC-SHA256
        corpo = await request.body()
        assinatura_esperada = hmac.new(segredo, corpo, hashlib.sha256).hexdigest()

        if assinatura_recebida != assinatura_esperada:
            print("🚨 Assinatura inválida no webhook.")
            raise HTTPException(status_code=403, detail="Assinatura inválida")

        dados = await request.json()

        if dados.get("type") == "payment":
            pagamento_id = dados["data"].get("id")
            pagamento = sdk.payment().get(pagamento_id)
            status = pagamento["response"]["status"]
            email_comprador = pagamento["response"]["payer"]["email"]

            if status == "approved":
                print(f"✅ Pagamento aprovado para: {email_comprador}")
                # Aqui você pode atualizar o banco, liberar conteúdo, enviar e-mail etc.

        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Erro no webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro ao processar webhook")
