from pydantic import BaseModel, Field

class QuoteOut(BaseModel):
    sell: float
    buy: float
    date: str
    id_account: str = Field(..., alias="id-account")

    class Config:
        # garante que o FastAPI use o alias no JSON de saída
        populate_by_name = True
        orm_mode = True
