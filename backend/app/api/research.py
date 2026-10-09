from datetime import datetime
import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.agent.graph import build_research_graph
from app.db.database import get_db
from app.db.models import (
    AgentRun,
    ResearchReport,
    Source,
)
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
)
async def create_research(
    request: ResearchRequest,
    db: Session = Depends(get_db),
):

    company_name = request.company_name.strip()

    if not company_name:
        raise HTTPException(
            status_code=400,
            detail="Company name cannot be empty.",
        )

    # ========================================================
    # 1. CREATE AGENT RUN
    # ========================================================

    agent_run = AgentRun(
        company_name=company_name,
        status="running",
        user_id=None,
        started_at=datetime.utcnow(),
    )

    db.add(agent_run)
    db.commit()
    db.refresh(agent_run)

    try:

        # ====================================================
        # 2. BUILD RESEARCH GRAPH
        # ====================================================

        graph = build_research_graph()

        # ====================================================
        # 3. INITIAL STATE
        # ====================================================

        initial_state = {
            "company_name": company_name,
            "errors": [],
        }

        # ====================================================
        # 4. RUN RESEARCH AGENT
        # ====================================================

        result = await graph.ainvoke(
            initial_state
        )

        agent_errors = result.get(
            "errors",
            []
        )

        # ====================================================
        # 5. GET GENERATED REPORT
        # ====================================================

        report_content = result.get(
            "report"
        )

        if not report_content:
            raise ValueError(
                "Agent completed without "
                "generating a report."
            )

        # ====================================================
        # 6. NORMALIZE REPORT
        # ====================================================
        #
        # Supported formats:
        # - Pydantic model
        # - dict
        # - JSON string
        # ====================================================

        if hasattr(
            report_content,
            "model_dump",
        ):

            report_json = (
                report_content.model_dump()
            )

            report_content_string = (
                report_content.model_dump_json()
            )

        elif isinstance(
            report_content,
            dict,
        ):

            report_json = report_content

            report_content_string = json.dumps(
                report_content
            )

        elif isinstance(
            report_content,
            str,
        ):

            try:

                report_json = json.loads(
                    report_content
                )

                report_content_string = (
                    report_content
                )

            except json.JSONDecodeError as error:

                raise ValueError(
                    "Generated report is not "
                    f"valid JSON: {error}"
                )

        else:

            raise ValueError(
                "Unsupported report type: "
                f"{type(report_content)}"
            )

        # ====================================================
        # 7. GET FINAL COMPANY NAME
        # ====================================================

        final_company_name = result.get(
            "company_name",
            company_name,
        )

        # ====================================================
        # 8. SAVE RESEARCH REPORT
        # ====================================================

        report = ResearchReport(
            company_name=final_company_name,
            report_content=report_content_string,
            report_json=report_json,
            user_id=None,
        )

        db.add(report)

        db.flush()

        # ====================================================
        # 9. SAVE SOURCES
        # ====================================================

        evidence = result.get(
            "evidence",
            []
        )

        saved_urls = set()

        for item in evidence:

            if not isinstance(
                item,
                dict,
            ):
                continue

            url = item.get(
                "url",
                "",
            )

            title = item.get(
                "title",
                "Unknown source",
            )

            if not url:
                continue

            url = str(
                url
            ).strip()

            if not url:
                continue

            if url in saved_urls:
                continue

            saved_urls.add(url)

            source = Source(
                url=url,
                title=title,
                report_id=report.id,
            )

            db.add(source)

        # ====================================================
        # 10. UPDATE AGENT RUN
        # ====================================================

        agent_run.status = "completed"

        agent_run.completed_at = (
            datetime.utcnow()
        )

        agent_run.report_id = report.id

        if agent_errors:

            agent_run.error_message = (
                "; ".join(
                    str(error)
                    for error in agent_errors
                )
            )

        # ====================================================
        # 11. COMMIT
        # ====================================================

        db.commit()

        db.refresh(report)

        return report

    except Exception as error:

        # ====================================================
        # AGENT FAILURE
        # ====================================================

        db.rollback()

        agent_run.status = "failed"

        agent_run.completed_at = (
            datetime.utcnow()
        )

        agent_run.error_message = str(
            error
        )

        db.add(agent_run)

        db.commit()

        raise HTTPException(
            status_code=502,
            detail=(
                "Research agent failed: "
                f"{error}"
            ),
        )