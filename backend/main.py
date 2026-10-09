"""FastAPI backend skeleton. Endpoints follow docs/api.md."""
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="ProofFix API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for now (stub). Replaced when the agent loop is built.
RUNS: dict[str, dict] = {}


class RunRequest(BaseModel):
    issue_text: str
    repo_url: str
    language: str = "python"
    max_attempts: int = 3


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/runs", status_code=201)
def create_run(req: RunRequest):
    run_id = "run_" + uuid.uuid4().hex[:6]
    RUNS[run_id] = {
        "run_id": run_id,
        "status": "queued",
        "current_step": None,
        "attempt": 0,
        "max_attempts": req.max_attempts,
        "created_at": now(),
        "result": None,
        "request": req.model_dump(),
    }
    return {"run_id": run_id, "status": "queued"}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    run = RUNS.get(run_id)
    if run is None:
        return JSONResponse(
            status_code=404,
            content={"error": "run_not_found", "message": "No run with that id"},
        )
    return {k: v for k, v in run.items() if k != "request"}
