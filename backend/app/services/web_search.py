from typing import Any

from tavily import TavilyClient

from app.config import settings


class WebSearchService:

    def __init__(self):

        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    async def search(
        self,
        query: str,
    ) -> list[dict[str, Any]]:

        response = self.client.search(
            query=query,
            search_depth="basic",
            max_results=5,
        )

        return response.get(
            "results",
            []
        )