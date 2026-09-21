from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from routers import records

app = FastAPI(title="AI Tool Usage Tracker")

app.include_router(records.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable"}
