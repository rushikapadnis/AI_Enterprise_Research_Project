from datetime import datetime

from pydantic import BaseModel


class ResearchRequest(BaseModel):
    company_name: str


class SourceResponse(BaseModel):
    id: int
    url: str
    title: str | None
    report_id: int

    model_config = {
        "from_attributes": True
    }


class ResearchResponse(BaseModel):
    id: int
    company_name: str
    report_content: str
    user_id: int
    created_at: datetime
    sources: list[SourceResponse] = []

    model_config = {
        "from_attributes": True
    }


# ============================================================
# Structured LLM Research Report
# ============================================================

class CompanyOverview(BaseModel):
    company: str
    ticker: str
    sector: str
    industry: str
    headquarters: str
    core_business: str


class RecentDevelopment(BaseModel):
    development: str
    date: str
    source: str
    business_relevance: str


class BusinessSignal(BaseModel):
    signal: str
    category: str
    evidence: str


class PotentialPainPoint(BaseModel):
    pain_point: str
    evidence: str
    reasoning: str


class PotentialOpportunity(BaseModel):
    opportunity: str
    evidence: str
    why_it_matters: str
    suggested_action: str


class RiskAndUnknown(BaseModel):
    risk: str
    evidence: str


class RecommendedNextAction(BaseModel):
    action: str
    reason: str


class StructuredResearchReport(BaseModel):
    executive_summary: list[str]

    company_overview: CompanyOverview

    recent_developments: list[RecentDevelopment]

    business_signals: list[BusinessSignal]

    potential_pain_points: list[PotentialPainPoint]

    potential_opportunities: list[PotentialOpportunity]

    risks_and_unknowns: list[RiskAndUnknown]

    recommended_next_actions: list[RecommendedNextAction]