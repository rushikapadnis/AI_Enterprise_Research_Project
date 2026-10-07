import asyncio

from app.services.llm_service import LLMService


async def main():

    service = LLMService()

    company_data = {
        "Name": "NVIDIA Corporation",
        "Symbol": "NVDA",
        "Sector": "Technology",
        "Industry": "Semiconductors",
        "Description": (
            "NVIDIA designs and develops accelerated "
            "computing platforms and software."
        ),
    }

    articles = [
        {
            "title": "NVIDIA announces new AI developments",
            "source": {
                "name": "Example News"
            },
            "publishedAt": "2026-09-15",
            "url": "https://example.com/article",
        }
    ]

    report = await service.generate_research(
        company_data,
        articles,
    )

    print("\n")
    print("=" * 60)
    print("AI RESEARCH REPORT")
    print("=" * 60)
    print(report)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())