# AI Enterprise Research & Action Agent

An AI-powered enterprise research application that generates structured
company intelligence briefs from company profile data, recent news, and
web search. The project combines a **Next.js frontend**, **FastAPI
backend**, **LangGraph workflow orchestration**, external research APIs,
and **PostgreSQL** persistence.

The intended user experience is simple: sign in, enter a company name,
and generate a research brief that organizes findings into an executive
summary, company overview, recent developments, business signals,
potential pain points, opportunities, risks, and recommended next
actions.

> **Evidence-first principle:** Research results should be treated as
> sourced evidence, not unquestionable facts. Review source links and
> verify important claims before making business, investment, or
> operational decisions.

------------------------------------------------------------------------

## Table of contents

-   [Features](#features)
-   [Architecture](#architecture)
-   [Research workflow](#research-workflow)
-   [Technology stack](#technology-stack)
-   [Project structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Configuration](#configuration)
-   [Local setup](#local-setup)
-   [API overview](#api-overview)
-   [Database](#database)
-   [Testing](#testing)
-   [Security and production
    readiness](#security-and-production-readiness)
-   [Troubleshooting](#troubleshooting)
-   [Roadmap](#roadmap)

------------------------------------------------------------------------

## Features

-   **Company research:** Retrieves company profile information through
    Alpha Vantage.
-   **Recent news collection:** Collects news articles through NewsAPI.
-   **Web research:** Uses Tavily to retrieve relevant web results.
-   **Agentic workflow:** Uses LangGraph nodes and conditional routing
    to plan and run the research stages.
-   **Evidence normalization:** Consolidates company information, news,
    and web results into a consistent evidence structure.
-   **Structured research reports:** Uses a Groq-powered LLM service to
    generate a report with defined sections.
-   **Source persistence:** Stores report source URLs and titles
    alongside the generated report.
-   **User accounts and login:** Provides user registration and JWT
    bearer-token login endpoints.
-   **Research history data model:** Persists research reports and
    agent-run status in PostgreSQL.
-   **Web dashboard:** Next.js interface for signing in and generating
    company research briefs.
-   **API documentation:** FastAPI interactive documentation is
    available at `/docs` when the backend is running.
-   **Health endpoints:** Root and health routes for basic service
    checks.

## Architecture

``` mermaid
flowchart TD
    U[User] --> FE[Next.js 16 / React 19 UI]
    FE -->|HTTP JSON + Bearer token| API[FastAPI]
    API --> AUTH[User and JWT Authentication]
    API --> GRAPH[LangGraph Research Workflow]
    GRAPH --> PLAN[Research Planner]
    PLAN --> COMPANY[Company Profile Service]
    COMPANY --> NEWS[News Service]
    NEWS --> WEB[Tavily Web Search]
    WEB --> NORMALIZE[Evidence Normalization]
    NORMALIZE --> LLM[Groq LLM Report Generation]
    LLM --> REPORT[Structured Research Report]
    API --> DB[(PostgreSQL)]
    REPORT --> DB
    DB --> SOURCES[Saved Sources and Agent Runs]
```

### Component responsibilities

  -----------------------------------------------------------------------
  Layer                   Technology              Responsibility
  ----------------------- ----------------------- -----------------------
  Frontend                Next.js, React,         Login and company
                          TypeScript, Tailwind    research dashboard
                          CSS                     

  API                     FastAPI, Pydantic       HTTP endpoints,
                                                  validation, dependency
                                                  injection

  Orchestration           LangGraph               Stateful research
                                                  workflow and
                                                  conditional routing

  LLM                     Groq                    Research planning and
                                                  report generation

  Company data            Alpha Vantage           Company profile and
                                                  overview data

  News                    NewsAPI                 Recent news articles

  Web search              Tavily                  Supplemental web
                                                  evidence

  Persistence             PostgreSQL, SQLAlchemy  Users, research
                                                  reports, sources, agent
                                                  runs

  Authentication          JWT bearer tokens       Authenticated API
                                                  requests
  -----------------------------------------------------------------------

## Research workflow

``` text
Company name
    ↓
Research request API
    ↓
LangGraph research planner
    ↓
Collect required evidence
    ├── Company profile (Alpha Vantage)
    ├── Recent news (NewsAPI)
    └── Web results (Tavily)
    ↓
Normalize evidence into a common structure
    ↓
Groq generates a structured research report
    ↓
Persist report, source URLs, and agent-run status
    ↓
Return the report to the frontend
```

The graph currently uses these workflow nodes:

1.  **Research Planner** --- decides which research sources are
    required.
2.  **Collect Company** --- retrieves company overview data.
3.  **Collect News** --- retrieves news evidence.
4.  **Collect Web Search** --- retrieves web evidence.
5.  **Normalize Evidence** --- converts collected material into a common
    structure.
6.  **Generate Report** --- generates the structured report from the
    available evidence.

The workflow routes between collection nodes based on the planner's
`required_sources` state. Actual source availability depends on valid
API keys, provider limits, and the company being researched.

## Report structure

The structured report schema includes:

-   Executive summary
-   Company overview
-   Recent developments
-   Business signals
-   Potential pain points
-   Potential opportunities
-   Risks and unknowns
-   Recommended next actions

The API also returns source records associated with the saved report.
Verify the original links and publication dates before relying on
generated conclusions.

## Technology stack

-   Python 3.11+ (the project has also been developed with a Python 3.12
    Conda environment; use a version compatible with the installed
    dependencies)
-   FastAPI and Uvicorn
-   LangGraph
-   Groq LLM API
-   Alpha Vantage API
-   NewsAPI
-   Tavily Search API
-   PostgreSQL
-   SQLAlchemy
-   Pydantic and pydantic-settings
-   HTTPX
-   Next.js 16
-   React 19
-   TypeScript
-   Tailwind CSS
-   npm

------------------------------------------------------------------------

## Project structure

``` text
AI_Enterprise_Research_Project/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py          # LangGraph construction and routing
│   │   │   ├── nodes.py          # Planner, collection, normalization, report nodes
│   │   │   ├── plan.py           # Research plan schema
│   │   │   └── state.py          # Shared workflow state
│   │   ├── api/
│   │   │   ├── agent/            # Agent-related API package
│   │   │   ├── auth.py           # Bearer-token user dependency
│   │   │   ├── research.py       # Research endpoint and persistence
│   │   │   └── users.py          # Registration and login endpoints
│   │   ├── db/
│   │   │   ├── database.py       # SQLAlchemy engine and DB session
│   │   │   └── models.py         # User, report, source, agent-run models
│   │   ├── schemas/
│   │   │   ├── research.py       # Request and structured report schemas
│   │   │   └── user.py           # User and token schemas
│   │   ├── services/
│   │   │   ├── auth_service.py   # Token helpers
│   │   │   ├── company_data.py   # Alpha Vantage integration
│   │   │   ├── company_resolver.py
│   │   │   ├── llm_service.py   # Groq report generation
│   │   │   ├── news_services.py # NewsAPI integration
│   │   │   └── web_search.py    # Tavily integration
│   │   ├── config.py             # Environment-based settings
│   │   └── main.py               # FastAPI application
│   ├── requirements.txt
│   └── test_*.py                 # Backend test scripts
└── frontend/
    ├── app/
    │   ├── login/page.tsx        # Login page
    │   ├── page.tsx              # Research dashboard
    │   ├── layout.tsx
    │   └── globals.css
    ├── lib/api.ts                # Frontend API helper
    ├── package.json
    └── next.config.ts
```

------------------------------------------------------------------------

## Prerequisites

Install the following before running the application:

-   Python 3.11 or 3.12
-   Node.js compatible with the Next.js version in
    `frontend/package.json`
-   npm
-   PostgreSQL
-   API keys for Alpha Vantage, NewsAPI, Groq, and Tavily

You need access to a PostgreSQL database and must configure the backend
environment before starting the API.

## Configuration

Create a `.env` file in the **`backend/` directory** for the backend
settings. The settings class loads `.env` from the process working
directory, so run Uvicorn from `backend/`.

``` env
APP_NAME=AI Enterprise Research & Action Agent
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/enterprise_research

ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
NEWS_API_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

JWT_SECRET_KEY=replace_with_a_long_random_secret
```

Use the exact variable names above; `pydantic-settings` maps these
environment variables to the settings fields in `backend/app/config.py`.

**Never commit `.env` or real API keys.** Keep `.env` out of version
control and use your deployment platform's secret/environment-variable
manager in hosted environments.

### Frontend API URL

Check `frontend/lib/api.ts` to confirm how the API base URL is selected.
If the frontend needs a configurable backend URL for deployment, define
a public environment variable such as `NEXT_PUBLIC_API_BASE_URL` and
wire it into the API helper. Do not assume that variable is already
supported without checking the code.

------------------------------------------------------------------------

## Local setup

### 1. Start PostgreSQL

Create a database, for example `enterprise_research`, and ensure the
credentials match `DATABASE_URL`.

The application uses SQLAlchemy models. The repository snapshot does not
include a database migration setup, so database tables must be created
through your existing database initialization procedure or a migration
workflow before using the API.

### 2. Set up the backend

Open PowerShell at the repository root:

``` powershell
cd backend

conda create -n fde-agent python=3.12 -y        
conda activate fde-agent   
                            

python -m pip install --upgrade pip
```

Install the backend dependencies. **Important:** the supplied
`backend/requirements.txt` is empty in this project snapshot. Populate
it with the dependencies used by the code before running the backend.
The imports indicate that the application needs, at minimum, packages
covering FastAPI, Uvicorn, SQLAlchemy, PostgreSQL connectivity
(`psycopg`), Pydantic settings, email validation, HTTPX, LangGraph, the
Groq/LangChain integration used by `llm_service.py`, and JWT support
used by `auth_service.py`. Confirm exact package names and versions from
those service files and your tested environment.

Create `backend/.env` using the configuration example above.

Start the API from the `backend` directory:

``` powershell
python -m uvicorn app.main:app --reload --port 8000
```

Open:

-   API root: http://127.0.0.1:8000/
-   Health check: http://127.0.0.1:8000/health
-   Swagger UI: http://127.0.0.1:8000/docs
-   OpenAPI schema: http://127.0.0.1:8000/openapi.json

### 3. Set up the frontend

Open a second PowerShell terminal at the repository root:

``` powershell
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000.

The FastAPI CORS configuration currently permits `http://localhost:3000`
and `http://127.0.0.1:3000`. Update the allowed origins for your actual
frontend domain before deploying.

------------------------------------------------------------------------

## API overview

The API routes are registered without an `/api` prefix in the current
backend code.

  -----------------------------------------------------------------------
  Method            Path              Description       Authentication
  ----------------- ----------------- ----------------- -----------------
  `GET`             `/`               API               No
                                      welcome/status    
                                      message           

  `GET`             `/health`         Basic health      No
                                      check             

  `POST`            `/users`          Register a user   No

  `POST`            `/users/login`    Log in and return No
                                      a bearer token    

  `POST`            `/research`       Generate and      Bearer token
                                      persist a company 
                                      research report   
  -----------------------------------------------------------------------

### Register a user

`POST /users`

``` json
{
  "email": "researcher@example.com",
  "password": "replace-with-a-strong-password"
}
```

A successful request returns the created user's ID, email, and creation
timestamp. Registering an email that already exists returns HTTP `409`.

### Log in

`POST /users/login`

``` json
{
  "email": "researcher@example.com",
  "password": "replace-with-a-strong-password"
}
```

A successful response returns a token:

``` json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

Send it to authenticated endpoints using:

``` http
Authorization: Bearer <jwt-token>
```

### Generate a research report

`POST /research`

``` json
{
  "company_name": "NVIDIA"
}
```

Include the bearer token in the request. The endpoint runs the LangGraph
workflow, saves the generated report and source URLs, and returns the
research response.

The response schema includes the report ID, company name, report
content, user ID field, creation timestamp, and source list. The
structured report is also stored in the database as JSON.

### Error behavior

-   `400` --- invalid/empty company name
-   `401` --- invalid or expired bearer token, or invalid login
-   `409` --- user already exists
-   `502` --- research workflow or report generation failed

For the exact live request and response schemas, use `/docs`.

------------------------------------------------------------------------

## Database

The SQLAlchemy models define these tables:

  Table                Purpose
  -------------------- ---------------------------------------------------
  `users`              User account records
  `research_reports`   Generated report content and structured JSON
  `sources`            Source URLs and titles linked to reports
  `agent_runs`         Research execution status, timestamps, and errors

The current research endpoint creates an `AgentRun`, runs the graph,
persists the report and unique source URLs, and marks the run as
completed or failed.

**Ownership note:** In the supplied implementation, report and agent-run
creation use `user_id=None` rather than associating the records with the
authenticated user. Do not present the current implementation as
providing complete per-user report isolation until that is fixed and
tested.

------------------------------------------------------------------------

## Testing

The backend contains individual test scripts, including:

-   `test_agent.py`
-   `test_company_api.py`
-   `test_company_service.py`
-   `test_db.py`
-   `test_llm_service.py`
-   `test_news_service.py`
-   `test_planner.py`
-   `test_web_search.py`

Run tests from `backend/` after installing the test dependencies and
configuring the required environment variables. Some tests may make live
API calls or require a working database; check each test before running
it.

Example:

``` powershell
cd backend
python -m pytest -v
```

The repository snapshot does not establish that every test is an
isolated, network-free unit test. Use mock responses and a dedicated
test database for a repeatable CI test suite.

------------------------------------------------------------------------

## Security and production readiness

This is an enterprise-oriented project, but **the supplied repository
snapshot should not be considered production-secure without additional
work**.

Before exposing it to real users:

-   **Hash passwords:** the current user service stores the supplied
    password directly in `password_hash` and compares it directly at
    login. Replace this with a strong password-hashing algorithm such as
    Argon2id or bcrypt.
-   **Review JWT settings:** use a high-entropy secret, set and validate
    token expiration, and handle token errors explicitly.
-   **Enforce user ownership:** associate every report and agent run
    with the authenticated user and enforce ownership checks when
    retrieving records.
-   **Avoid leaking internals:** return safe client-facing error
    messages; log detailed errors securely on the server rather than
    returning raw exception strings.
-   **Protect secrets:** use environment variables or a secret manager;
    rotate keys if they have been exposed.
-   **Harden deployment:** restrict CORS to trusted origins, add rate
    limits, request-size limits, timeouts, and abuse protection.
-   **Validate external data:** treat retrieved pages, news
    descriptions, and company data as untrusted input. Guard against
    prompt injection and require evidence for claims.
-   **Improve source traceability:** preserve source URLs, titles,
    publication dates, and evidence-to-claim mapping where possible.
-   **Add database migrations:** use Alembic or another controlled
    migration process instead of relying on ad hoc table creation.
-   **Add observability:** use structured logs, request IDs, provider
    latency/error metrics, and a proper readiness check that verifies
    required dependencies.
-   **Add tests:** cover authentication, authorization, source failures,
    rate limits, malformed model output, and end-to-end research
    requests.
-   **Review privacy and licensing:** disclose use of third-party
    LLM/search/data providers and comply with their terms.

------------------------------------------------------------------------

## Troubleshooting

  --------------------------------------------------------------------------------------------
  Problem                             What to check
  ----------------------------------- --------------------------------------------------------
  Settings validation fails at        Confirm `backend/.env` exists, required variables are
  startup                             present, and Uvicorn is launched from `backend/`.

  `ModuleNotFoundError: app`          Run Uvicorn from `backend/` using
                                      `python -m uvicorn app.main:app --reload --port 8000`.

  PostgreSQL connection error         Check that PostgreSQL is running and `DATABASE_URL` has
                                      the correct driver, credentials, host, port, and
                                      database name.

  `psycopg` or PostgreSQL driver      Install and configure the PostgreSQL driver referenced
  error                               by your `DATABASE_URL`.

  Frontend cannot call the API        Confirm the API is running, inspect
                                      `frontend/lib/api.ts`, and check CORS origins and the
                                      configured API base URL.

  Research endpoint returns `401`     Log in again and send
                                      `Authorization: Bearer <access_token>`.

  Provider returns no data or an      Check API key validity, provider quotas, company symbol
  error                               resolution, and provider response messages.

  Research endpoint returns `502`     Inspect backend logs for the failing graph node or
                                      provider; do not expose raw internal errors publicly.

  Dependencies cannot be installed    Populate the currently empty `backend/requirements.txt`
                                      with tested, pinned dependencies.
  --------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## Roadmap

-   Pin backend dependencies and add reproducible environment setup.
-   Add Alembic migrations and database initialization instructions.
-   Implement secure password hashing and expiring JWTs.
-   Link reports and agent runs to the authenticated user and enforce
    ownership.
-   Add source citations at the individual claim level.
-   Add retries, timeouts, and graceful degradation for external
    providers.
-   Add deterministic tests, CI checks, and production deployment
    configuration.
-   Add report history and report retrieval endpoints with access
    control.
-   Add deployment-specific environment configuration and monitoring.

------------------------------------------------------------------------

