from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import get_db
from models import UsageRecord
from schemas import TeamSummary

router = APIRouter(tags=["summary"])


@router.get("/summary", response_model=list[TeamSummary])
def team_summary(db: Session = Depends(get_db)):
    # GROUP BY in the database: 860 rows collapse to 5 before they cross the wire.
    stmt = (
        select(
            UsageRecord.team,
            func.sum(UsageRecord.tokens).label("total_tokens"),
            func.sum(UsageRecord.cost).label("total_cost"),
            func.count().label("record_count"),
        )
        .group_by(UsageRecord.team)
        .order_by(func.sum(UsageRecord.tokens).desc())
    )
    return db.execute(stmt).all()
