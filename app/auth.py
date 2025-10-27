import jwt
from fastapi import Header, HTTPException
from .config import settings


def require_auth(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,
                            detail="Missing Authorization header")

    token = authorization.split(" ")[1]
    try:
        if settings.jwt_secret:
            payload = jwt.decode(token,
                                 settings.jwt_secret,
                                 algorithms=[settings.jwt_algorithm])
        else:
            # decodifica sem validar assinatura se não houver chave definida
            payload = jwt.decode(token, options={"verify_signature": False})

        account_id = (payload.get("id-account") or payload.get("account_id")
                      or payload.get("sub") or payload.get("id"))
        if not account_id:
            raise HTTPException(status_code=401,
                                detail="Invalid token payload")

        return account_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
