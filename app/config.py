from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # porta do uvicorn (só para rodar local)
    port: int = 8083

    # API de câmbio (sem chave por padrão)
    rates_base_url: str = "https://api.exchangerate.host"

    # spread para calcular buy/sell (ex.: 0.02 = ±1% em cada lado)
    spread: float = 0.02

    # verificação de JWT (opcional). Se não informar, só decodifica sem validar assinatura
    jwt_secret: str | None = None          # HS256
    jwt_public_key: str | None = None      # RS256/ES256 (PEM)
    jwt_algorithm: str | None = None       # "HS256", "RS256", ...

    class Config:
        env_prefix = "EXCHANGE_"
        env_file = ".env"

settings = Settings()
