import asyncio
import json

from app.agent.graph import build_research_graph


async def main():

    graph = build_research_graph()

    initial_state = {
        "company_name": "NVIDIA",
        "errors": [],
    }

    result = await graph.ainvoke(
        initial_state
    )

    print("\n")
    print("=" * 70)
    print("STRUCTURED AGENT RESULT")
    print("=" * 70)

    print("\nCompany:")
    print(
        result.get("company_name")
    )

    print("\nTicker:")
    print(
        result.get("ticker")
    )

    print("\nRequired Sources:")
    print(
        result.get("required_sources")
    )

    print("\nEvidence Count:")
    print(
        len(
            result.get(
                "evidence",
                []
            )
        )
    )

    print("\nStructured Report:")

    report = result.get(
        "report"
    )

    if report:

        parsed_report = report.model_dump() 
        

        print(
            json.dumps(
                parsed_report,
                indent=2
            )
        )

    print("\nErrors:")

    print(
        result.get(
            "errors",
            []
        )
    )

    print("=" * 70)


if __name__ == "__main__":

    asyncio.run(main())