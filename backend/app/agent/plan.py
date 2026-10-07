from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):

    company: bool = Field(
        description="Whether company information is required."
    )

    news: bool = Field(
        description="Whether recent news is required."
    )

    search: bool = Field(
        description="Whether web search is required."
    )