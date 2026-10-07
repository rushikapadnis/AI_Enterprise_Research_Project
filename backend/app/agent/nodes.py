import json

from app.agent.plan import ResearchPlan
from app.agent.state import ResearchState

from app.services.company_data import CompanyDataService
from app.services.company_resolver import CompanyResolver
from app.services.news_service import NewsService
from app.services.web_search import WebSearchService
from app.services.llm_service import LLMService


async def research_planner(
    state: ResearchState,
) -> ResearchState:

    company_name = state["company_name"]

    llm_service = LLMService()

    prompt = f"""
You are an enterprise research planning agent.

The user wants a research brief about:

{company_name}

Decide which research sources are required.

Available sources:

company:
Company profile, sector, industry and business information.

news:
Recent company developments and announcements.

search:
Broader web research, competitors, industry trends and
technology developments.

Return ONLY valid JSON.

The JSON MUST have exactly these fields:

{{
    "company": true,
    "news": true,
    "search": true
}}

Do not add any explanation.
Do not use markdown.
Do not use code fences.

For a comprehensive company research request,
select the useful sources.
"""

    response = await llm_service.llm.ainvoke(
        prompt
    )

    raw_content = response.content.strip()

    if raw_content.startswith("```"):

        raw_content = raw_content.replace(
            "```json",
            ""
        )

        raw_content = raw_content.replace(
            "```",
            ""
        )

        raw_content = raw_content.strip()

    try:

        parsed_plan = json.loads(
            raw_content
        )

        plan = ResearchPlan.model_validate(
            parsed_plan
        )

    except Exception as error:

        raise ValueError(
            f"Invalid research plan returned by LLM: {error}"
        )

    required_sources = []

    if plan.company:
        required_sources.append("company")

    if plan.news:
        required_sources.append("news")

    if plan.search:
        required_sources.append("search")

    if not required_sources:

        required_sources = [
            "company",
            "news",
        ]

    return {
        **state,
        "required_sources": required_sources,
    }


async def collect_company(
    state: ResearchState,
) -> ResearchState:

    errors = list(
        state.get("errors", [])
    )

    try:

        resolver = CompanyResolver()

        ticker = resolver.resolve(
            state["company_name"]
        )

        company_service = CompanyDataService()

        company_data = await company_service.get_company(
            ticker
        )

        return {
            **state,
            "ticker": ticker,
            "company_data": company_data,
            "errors": errors,
        }

    except Exception as error:

        errors.append(
            f"Company data collection failed: {error}"
        )

        return {
            **state,
            "errors": errors,
        }


async def collect_news(
    state: ResearchState,
) -> ResearchState:

    errors = list(
        state.get("errors", [])
    )

    try:

        news_service = NewsService()

        articles = await news_service.search_news(
            state["company_name"]
        )

        return {
            **state,
            "articles": articles,
            "errors": errors,
        }

    except Exception as error:

        errors.append(
            f"News collection failed: {error}"
        )

        return {
            **state,
            "articles": [],
            "errors": errors,
        }


async def collect_web_search(
    state: ResearchState,
) -> ResearchState:

    errors = list(
        state.get("errors", [])
    )

    try:

        search_service = WebSearchService()

        query = (
            f"{state['company_name']} "
            "latest business developments "
            "technology competitors industry"
        )

        results = await search_service.search(
            query
        )

        return {
            **state,
            "search_results": results,
            "errors": errors,
        }

    except Exception as error:

        errors.append(
            f"Web search failed: {error}"
        )

        return {
            **state,
            "search_results": [],
            "errors": errors,
        }
def normalize_evidence(
    state: ResearchState,
) -> ResearchState:

    evidence = []

    # ---------------------------------------------
    # Company evidence
    # ---------------------------------------------

    company_data = state.get("company_data", {})

    if company_data:

        company_name = company_data.get(
            "Name",
            state["company_name"],
        )

        description = company_data.get(
            "Description",
            "",
        )

        evidence.append(
            {
                "type": "company",
                "title": f"{company_name} company profile",
                "url": "",
                "content": description,
            }
        )

    # ---------------------------------------------
    # News evidence
    # ---------------------------------------------

    for article in state.get("articles", []):

        evidence.append(
            {
                "type": "news",
                "title": article.get(
                    "title",
                    "Untitled article",
                ),
                "url": article.get(
                    "url",
                    "",
                ),
                "content": article.get(
                    "description",
                    "",
                ),
                "source": article.get(
                    "source",
                    {},
                ).get(
                    "name",
                    "Unknown",
                ),
                "published_at": article.get(
                    "publishedAt",
                    "",
                ),
            }
        )

    # ---------------------------------------------
    # Web search evidence
    # ---------------------------------------------

    for result in state.get(
        "search_results",
        [],
    ):

        evidence.append(
            {
                "type": "web",
                "title": result.get(
                    "title",
                    "Untitled result",
                ),
                "url": result.get(
                    "url",
                    "",
                ),
                "content": result.get(
                    "content",
                    "",
                ),
            }
        )

    return {
        **state,
        "evidence": evidence,
    }

async def generate_report(
    state: ResearchState
) -> ResearchState:

    llm_service = LLMService()

    company_data = state.get(
        "company_data",
        {}
    )

    evidence = state.get(
        "evidence",
        []
    )

    errors = state.get(
        "errors",
        []
    )

    structured_report = (
        await llm_service.generate_research(
            company_data=company_data,
            evidence=evidence,
        )
    )

    report_json = structured_report
    

    return {
        **state,
        "report": report_json,
        "errors": errors,
    }