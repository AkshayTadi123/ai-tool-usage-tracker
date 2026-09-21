from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import UsageRecord
from schemas import UsageRecordCreate, UsageRecordOut

router = APIRouter(prefix="/records", tags=["records"])


@router.get("", response_model=list[UsageRecordOut])
def list_records(
    team: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(UsageRecord)
    if team:
        stmt = stmt.where(UsageRecord.team == team)
    # id is the tiebreaker: used_on alone leaves ties in undefined order,
    # which lets rows drift between pages.
    stmt = (
        stmt.order_by(UsageRecord.used_on.desc(), UsageRecord.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return db.scalars(stmt).all()


@router.post("", response_model=UsageRecordOut, status_code=status.HTTP_201_CREATED)
def create_record(payload: UsageRecordCreate, db: Session = Depends(get_db)):
    record = UsageRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)  # reload so the database-assigned id is populated
    return record
