import asyncio

from app.agent.nodes import research_planner


async def main():

    state = {
        "company_name": "NVIDIA",
        "errors": [],
    }

    result = await research_planner(
        state
    )

    print("\n")
    print("=" * 60)
    print("RESEARCH PLAN")
    print("=" * 60)

    print(
        "Company:",
        result.get("company_name")
    )

    print(
        "Required Sources:",
        result.get("required_sources")
    )

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())