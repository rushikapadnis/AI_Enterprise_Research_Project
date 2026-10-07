import json
from typing import Any

from langchain_groq import ChatGroq

from app.config import settings
from app.schemas.research import StructuredResearchReport


class LLMService:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model="openai/gpt-oss-20b",
            temperature=0,
            max_tokens=4096,
        )

    async def generate_research(
        self,
        company_data: dict[str, Any],
        evidence: list[dict[str, Any]],
    ) -> StructuredResearchReport:

        company_name = company_data.get(
            "Name",
            "Unknown"
        )

        symbol = company_data.get(
            "Symbol",
            "Unknown"
        )

        sector = company_data.get(
            "Sector",
            "Unknown"
        )

        industry = company_data.get(
            "Industry",
            "Unknown"
        )

        description = company_data.get(
            "Description",
            "No description available."
        )

        headquarters = company_data.get(
            "Address",
            "Unknown"
        )
        # ----------------------------------------------------
        # Build evidence
        # ----------------------------------------------------

        evidence_text = ""

        for index, item in enumerate(
            evidence,
            start=1
        ):

            evidence_text += f"""
Evidence {index}
==============================

Type:
{item.get("type", "unknown")}

Title:
{item.get("title", "Unknown")}

Source:
{item.get("source", "Unknown")}

Published:
{item.get("published_at", "Unknown")}

URL:
{item.get("url", "")}

Content:
{item.get("content", "")}

"""

        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are an enterprise research analyst.

Research company:

{company_name}

Use ONLY the supplied company information and evidence.

IMPORTANT RULES:

1. Never invent facts.
2. Never invent sources.
3. Never invent URLs.
4. Clearly distinguish evidence from analytical conclusions.
5. If evidence is insufficient, say "Insufficient evidence."
6. Do not treat speculation as fact.
7. Do not make unsupported financial predictions.
8. For regulatory or political topics, remain factual and neutral.
9. Return ONLY valid JSON.
10. Do not use markdown.
11. Do not use code fences.

==================================================
COMPANY INFORMATION
==================================================

Company:
{company_name}

Ticker:
{symbol}

Sector:
{sector}

Industry:
{industry}

Headquarters:
{headquarters}

Description:
{description}

==================================================
EVIDENCE
==================================================

{evidence_text}

==================================================
REQUIRED JSON
==================================================

Return JSON using EXACTLY this structure:

{{
  "executive_summary": [
    "finding 1",
    "finding 2",
    "finding 3"
  ],

  "company_overview": {{
    "company": "{company_name}",
    "ticker": "{symbol}",
    "sector": "{sector}",
    "industry": "{industry}",
    "headquarters": "{headquarters}",
    "core_business": "..."
  }},

  "recent_developments": [
    {{
      "development": "...",
      "date": "...",
      "source": "...",
      "business_relevance": "..."
    }}
  ],

  "business_signals": [
    {{
      "signal": "...",
      "category": "technology",
      "evidence": "..."
    }}
  ],

  "potential_pain_points": [
    {{
      "pain_point": "...",
      "evidence": "...",
      "reasoning": "..."
    }}
  ],

  "potential_opportunities": [
    {{
      "opportunity": "...",
      "evidence": "...",
      "why_it_matters": "...",
      "suggested_action": "..."
    }}
  ],

  "risks_and_unknowns": [
    {{
      "risk": "...",
      "evidence": "..."
    }}
  ],

  "recommended_next_actions": [
    {{
      "action": "...",
      "reason": "..."
    }}
  ]
}}

Only include information supported by the supplied evidence.
"""

        # ----------------------------------------------------
        # Call Groq
        # ----------------------------------------------------

        try:

            response = await self.llm.ainvoke(
                prompt
            )

        except Exception as error:

            raise ValueError(
                f"Groq LLM request failed: {error}"
            ) from error
        # ----------------------------------------------------
        # Extract response
        # ----------------------------------------------------

        content = response.content

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, str):

                    text_parts.append(item)

                elif isinstance(item, dict):

                    if item.get("type") == "text":

                        text_parts.append(
                            item.get("text", "")
                        )

            content = "\n".join(
                text_parts
            )

        if content is None:

            content = ""

        content = str(content).strip()

        if not content:

            metadata = getattr(
                response,
                "response_metadata",
                {}
            )

            raise ValueError(
                "Groq returned empty response. "
                f"Metadata: {metadata}"
            )

        # ----------------------------------------------------
        # Remove accidental code fences
        # ----------------------------------------------------

        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        # ----------------------------------------------------
        # JSON parsing
        # ----------------------------------------------------

        try:

            parsed = json.loads(
                content
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                "Groq returned invalid JSON: "
                f"{error}"
            ) from error

        # ----------------------------------------------------
        # Pydantic validation
        # ----------------------------------------------------

        try:

            report = (
                StructuredResearchReport
                .model_validate(parsed)
            )

        except Exception as error:

            raise ValueError(
                "LLM output failed schema validation: "
                f"{error}"
            ) from error

        return report