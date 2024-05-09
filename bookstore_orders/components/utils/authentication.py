from functools import wraps
from fastapi import Header, HTTPException
import jwt
from datetime import datetime, timedelta

from bookstore_orders.components.config import envs


# Função para verificar o token JWT
def verify_token(token: str) -> bool:
    try:
        # Decodifica o token usando a chave secreta
        payload = jwt.decode(token, envs.SECRET_KEY, algorithms=["HS256"])

        # Verifica se o token está dentro do período de validade
        # if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
        #     return False

        # Verifica se o token contém um campo específico (por exemplo, user_id)
        if "user_id" not in payload:
            return False

        return True
    except jwt.ExpiredSignatureError:
        # O token expirou
        return False
    except jwt.InvalidTokenError:
        # O token é inválido
        return False


# Decorador para verificar a autenticação
def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Obtenha o token de autorização do cabeçalho da solicitação
        authorization = kwargs.get("authorization", None)
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token")

        # Verifique o token de autenticação
        token = authorization.replace("Bearer ", "")
        if not verify_token(token):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        # Se a autenticação for bem-sucedida, chame a função de rota principal
        return await func(*args, **kwargs)

    return wrapper
