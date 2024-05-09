import jwt
from bookstore_orders.components.config import envs

# Definir o token
token = ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDU2In0"
         ".8fYhfuMUT3ZM28iG2lRiAWqo7vL8g1_fGSyVp3rHChw")

# Extrair o JWT do prefixo "Bearer"
jwt_token = token.split(" ")[1]

ALGORITHM = "HS256"

options = {
        'verify_exp': False,  # Skipping expiration date check
        'verify_aud': False
        }

# Decodificar e verificar o token
try:
    payload = jwt.decode(jwt_token, '8fYhfuMUT3ZM28iG2lRiAWqo7vL8g1_fGSyVp3rHChw', algorithms=[ALGORITHM], options=options)
    print("Token válido!")
    print("Payload:", payload)
except jwt.ExpiredSignatureError:
    print("Token expirado!")
except jwt.InvalidTokenError:
    print("Token inválido!")
