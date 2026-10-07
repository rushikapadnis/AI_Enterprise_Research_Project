from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

#from app.agent.graph import build_research_graph
from app.db.database import get_db
from app.db.models import ResearchReport, Source

from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)

#from app.api.auth import get_current_user

from app.services.company_data import CompanyDataService
from app.services.company_resolver import CompanyResolver

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
    #current_user: User = Depends(get_current_user),
):

    # ==================================================
    # 1. Build LangGraph
    # ==================================================

  #  graph = build_research_graph()

    # ==================================================
    # 2. Initial State
    # ==================================================

    initial_state = {
        "company_name": request.company_name,
        "errors": [],
    }

    # ==================================================
    # 3. Execute Agent
    # ==================================================

    try:

        result = await graph.ainvoke(
            initial_state
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Agent execution failed: {error}",
        )

    # ==================================================
    # 4. Validate Report
    # ==================================================

    report_content = result.get(
        "report"
    )

    if not report_content:

        raise HTTPException(
            status_code=502,
            detail="Agent completed without generating a report.",
        )

    # ==================================================
    # 5. Create Research Report
    # ==================================================

    company_name = result.get(
        "company_name",
        request.company_name,
    )

    report = ResearchReport(
        company_name=company_name,
        report_content=report_content,
        user_id=current_user.id,  # Temporary until JWT authentication
    )

    db.add(report)

    # Flush gives us report.id before commit
    db.flush()

    # ==================================================
    # 6. Save Evidence Sources
    # ==================================================

    evidence = result.get(
        "evidence",
        []
    )

    for item in evidence:

        url = item.get(
            "url",
            ""
        )

        title = item.get(
            "title",
            "Unknown source"
        )

        # Don't save evidence that has no URL
        if not url:
            continue

        source = Source(
            url=url,
            title=title,
            report_id=report.id,
        )

        db.add(source)

    # ==================================================
    # 7. Commit Everything
    # ==================================================

    db.commit()

    # ==================================================
    # 8. Refresh Report
    # ==================================================

    db.refresh(report)

    # ==================================================
    # 9. Return Response
    # ==================================================

    return report