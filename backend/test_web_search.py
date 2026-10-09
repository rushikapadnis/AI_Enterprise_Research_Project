import asyncio

from app.services.web_search import WebSearchService


async def main():

    service = WebSearchService()

    results = await service.search(
        "NVIDIA latest business developments"
    )

    print(
        "Number of results:",
        len(results)
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n----------------------")

        print(
            "Result:",
            index
        )

        print(
            "Title:",
            result.get("title")
        )

        print(
            "URL:",
            result.get("url")
        )

        print(
            "Content:",
            result.get("content")
        )


if __name__ == "__main__":
    asyncio.run(main())