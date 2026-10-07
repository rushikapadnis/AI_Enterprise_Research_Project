from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    collect_company,
    collect_news,
    collect_web_search,
    generate_report,
    normalize_evidence,
    research_planner,
)

from app.agent.state import ResearchState


def route_after_planner(
    state: ResearchState,
):
    """
    Decide which data collection node should run first.
    """

    sources = state.get(
        "required_sources",
        [],
    )

    if "company" in sources:
        return "collect_company"

    if "news" in sources:
        return "collect_news"

    if "search" in sources:
        return "collect_web_search"

    return "normalize_evidence"


def route_after_company(
    state: ResearchState,
):
    """
    Decide what should run after company data collection.
    """

    sources = state.get(
        "required_sources",
        []
    )

    if "news" in sources:
        return "collect_news"

    if "search" in sources:
        return "collect_web_search"

    return "normalize_evidence"


def route_after_news(
    state: ResearchState,
):
    """
    Decide what should run after news collection.
    """

    sources = state.get(
        "required_sources",
        []
    )

    if "search" in sources:
        return "collect_web_search"

    return "normalize_evidence"


def build_research_graph():

    # ---------------------------------------------
    # Create graph
    # ---------------------------------------------

    graph = StateGraph(
        ResearchState
    )

    # ---------------------------------------------
    # Add nodes
    # ---------------------------------------------

    graph.add_node(
        "research_planner",
        research_planner,
    )

    graph.add_node(
        "collect_company",
        collect_company,
    )

    graph.add_node(
        "collect_news",
        collect_news,
    )

    graph.add_node(
        "collect_web_search",
        collect_web_search,
    )

    graph.add_node(
        "normalize_evidence",
        normalize_evidence,
    )

    graph.add_node(
        "generate_report",
        generate_report,
    )

    # ---------------------------------------------
    # START → Planner
    # ---------------------------------------------

    graph.add_edge(
        START,
        "research_planner",
    )

    # ---------------------------------------------
    # Planner → Collection
    # ---------------------------------------------

    graph.add_conditional_edges(
        "research_planner",
        route_after_planner,
        {
            "collect_company": "collect_company",
            "collect_news": "collect_news",
            "collect_web_search": "collect_web_search",
            "normalize_evidence": "normalize_evidence",
        },
    )

    # ---------------------------------------------
    # Company → Next Collection
    # ---------------------------------------------

    graph.add_conditional_edges(
        "collect_company",
        route_after_company,
        {
            "collect_news": "collect_news",
            "collect_web_search": "collect_web_search",
            "normalize_evidence": "normalize_evidence",
        },
    )

    # ---------------------------------------------
    # News → Next Collection
    # ---------------------------------------------

    graph.add_conditional_edges(
        "collect_news",
        route_after_news,
        {
            "collect_web_search": "collect_web_search",
            "normalize_evidence": "normalize_evidence",
        },
    )

    # ---------------------------------------------
    # Web Search → Evidence Normalization
    # ---------------------------------------------

    graph.add_edge(
        "collect_web_search",
        "normalize_evidence",
    )

    # ---------------------------------------------
    # Evidence → LLM
    # ---------------------------------------------

    graph.add_edge(
        "normalize_evidence",
        "generate_report",
    )

    ## LLM → END
    # ---------------------------------------------

    graph.add_edge(
        "generate_report",
        END,
    )

    # ---------------------------------------------
    # Compile
    # ---------------------------------------------

    return graph.compile()