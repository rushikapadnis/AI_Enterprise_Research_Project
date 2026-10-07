import asyncio

from app.services.news_services import NewsService


async def main():

    service = NewsService()

    articles = await service.search_news(
        "NVIDIA"
    )

    print(
        "Number of articles:",
        len(articles)
    )

    for article in articles:

        print("\n--------------------")

        print(
            "Title:",
            article.get("title")
        )

        print(
            "Source:",
            article.get("source", {}).get("name")
        )

        print(
            "Published:",
            article.get("publishedAt")
        )

        print(
            "URL:",
            article.get("url")
        )


if __name__ == "__main__":
    asyncio.run(main())