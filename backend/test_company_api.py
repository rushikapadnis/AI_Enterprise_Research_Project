import asyncio

import httpx

from app.config import settings


async def main():

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "OVERVIEW",
        "symbol": "NVDA",
        "apikey": settings.alpha_vantage_api_key,
    }

    async with httpx.AsyncClient(timeout=30) as client:

        response = await client.get(
            url,
            params=params,
        )

        print("HTTP STATUS:", response.status_code)

        data = response.json()

        print(data)


asyncio.run(main())