from typing import Any

import httpx

from app.config import settings


class NewsService:

    BASE_URL = "https://newsapi.org/v2/everything"

    async def search_news(
        self,
        company_name: str,
    ) -> list[dict[str, Any]]:

        params = {
            "q": company_name,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 5,
            "apiKey": settings.news_api_key,
        }

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

        if data.get("status") != "ok":
            raise ValueError(
                f"News API error: {data.get('message', 'Unknown error')}"
            )

        articles = data.get(
            "articles",
            []
        )

        return articles