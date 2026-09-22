import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from routers import records, summary

app = FastAPI(title="AI Tool Usage Tracker")

# The Angular dev server is a different origin (:4200 vs :8000), so the browser
# blocks requests unless the API opts in. curl is unaffected - this is a browser rule.
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:4200").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records.router)
app.include_router(summary.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable"}
