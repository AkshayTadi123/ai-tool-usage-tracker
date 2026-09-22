from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import get_db
from models import UsageRecord
from schemas import TeamSummary, UserTotal

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


@router.get("/top-users", response_model=list[UserTotal])
def top_users(
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # Grouped by (user_name, team) so the team is selectable; each user is on
    # exactly one team, so this adds no extra groups.
    stmt = (
        select(
            UsageRecord.user_name,
            UsageRecord.team,
            func.sum(UsageRecord.tokens).label("total_tokens"),
            func.sum(UsageRecord.cost).label("total_cost"),
        )
        .group_by(UsageRecord.user_name, UsageRecord.team)
        .order_by(func.sum(UsageRecord.tokens).desc())
        .limit(limit)
    )
    return db.execute(stmt).all()
