from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8083

    rates_base_url: str = "https://api.exchangerate.host"

    spread: float = 0.02

    jwt_secret: str | None = None
    jwt_public_key: str | None = None
    jwt_algorithm: str = "HS256"

    class Config:
        env_prefix = "EXCHANGE_"
        env_file = ".env"


settings = Settings()
