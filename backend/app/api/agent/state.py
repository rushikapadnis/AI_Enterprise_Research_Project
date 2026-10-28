from typing import Any, TypedDict


class ResearchState(TypedDict, total=False):

    # User request
    company_name: str

    # Company resolution
    ticker: str

    # Research data
    company_data: dict[str, Any]

    # News evidence
    articles: list[dict[str, Any]]

    # Web evidence
    search_results: list[dict[str, Any]]

    # Unified evidence
    evidence: list[dict[str, Any]]

    # Agent planning
    required_sources: list[str]

    # Final output
    report: str

    # Errors
    errors: list[str]