from fastapi import Request, HTTPException
import jwt
from app.config import settings

async def require_auth(request: Request) -> dict:
    # 1) Preferir o header que o gateway já inseriu
    account_id = request.headers.get("id-account")
    if account_id:
        return {"id-account": str(account_id)}

    # 2) Fallback: pegar do Bearer token
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")

    token = auth.split()[1]
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS512"],
            options={"verify_aud": False},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")

    account_id = claims.get("id-account") or claims.get("id") or claims.get("sub")
    if not account_id:
        raise HTTPException(status_code=400, detail="missing account id")

    return {"id-account": str(account_id)}