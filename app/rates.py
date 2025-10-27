import httpx
from .config import settings
import logging

logging.basicConfig(level=logging.INFO)


async def get_exchange_rate(base: str, target: str):
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    logging.info(f"Fetching exchange rate from: {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        data = response.json()
        logging.info(f"Response: {data}")

    if "rates" not in data or target.upper() not in data["rates"]:
        logging.warning(f"No rates found for {base}/{target}")
        return None

    rate = data["rates"][target.upper()]
    spread = settings.spread
    return {
        "base": base.upper(),
        "target": target.upper(),
        "rate": rate,
        "buy": round(rate * (1 + spread), 6),
        "sell": round(rate * (1 - spread), 6),
    }
