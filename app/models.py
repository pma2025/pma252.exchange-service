from pydantic import BaseModel


class ExchangeResponse(BaseModel):
    base: str
    target: str
    rate: float
    buy: float
    sell: float


class ErrorResponse(BaseModel):
    detail: str
