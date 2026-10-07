from typing import Any

import httpx

from app.config import settings


class CompanyDataService:

    BASE_URL = "https://www.alphavantage.co/query"

    async def get_company(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": settings.alpha_vantage_api_key,
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

        # Alpha Vantage can return an error with HTTP 200.
        if "Error Message" in data:
            raise ValueError(
                f"Company API error: {data['Error Message']}"
            )

        # Alpha Vantage can return a rate-limit message.
        if "Note" in data:
            raise ValueError(
                f"Company API limit: {data['Note']}"
            )

        return data