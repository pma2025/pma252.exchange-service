import datetime as dt
import httpx

async def fetch_rate(from_curr: str, to_curr: str) -> tuple[float, str]:
    """
    Busca a cotação de from_curr->to_curr em provedores públicos e
    entende alguns formatos de resposta diferentes.
    Retorna (rate, date_iso). Lança RuntimeError se não conseguir extrair.
    """
    f = from_curr.upper()
    t = to_curr.upper()

    # 1) exchangerate.host (forma A: /convert)
    url_a = f"https://api.exchangerate.host/convert?from={f}&to={t}"
    # 2) frankfurter.app (forma B: /latest?from=&to=)
    url_b = f"https://api.frankfurter.app/latest?from={f}&to={t}"
    # 3) awesomeapi (forma C: /{from}-{to}/1) – retorna lista
    url_c = f"https://economia.awesomeapi.com.br/json/last/{f}-{t}"

    async with httpx.AsyncClient(timeout=10) as client:
        # tente A
        try:
            r = await client.get(url_a)
            data = r.json()
            # esperado: {"success":true, "info":{"rate": X}, "date":"YYYY-MM-DD", ...}
            rate = float(data.get("info", {}).get("rate"))
            date = data.get("date") or dt.date.today().isoformat()
            if rate > 0:
                return rate, date
        except Exception:
            pass

        # tente B
        try:
            r = await client.get(url_b)
            data = r.json()
            # esperado: {"amount":1,"base":"USD","date":"YYYY-MM-DD","rates":{"BRL":5.1}}
            rates = data.get("rates") or {}
            if t in rates:
                rate = float(rates[t])
                date = data.get("date") or dt.date.today().isoformat()
                if rate > 0:
                    return rate, date
        except Exception:
            pass

        # tente C
        try:
            r = await client.get(url_c)
            data = r.json()
            # esperado: {"USDBRL":{"bid":"5.18", "create_date":"2025-10-04 16:30:00", ...}}
            key = f"{f}{t}"
            if isinstance(data, dict) and key in data:
                item = data[key]
                rate = float(item.get("bid") or 0)
                date = (item.get("create_date") or item.get("timestamp")
                        or dt.date.today().isoformat())
                if rate > 0:
                    return rate, date
        except Exception:
            pass

    # nada deu certo
    raise RuntimeError("Provider schema not recognized or provider error")
