"""Pydantic models for request and response bodies."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UsageRecordCreate(BaseModel):
    """Request body for POST /records. No id: the database assigns it."""

    user_name: str = Field(min_length=1, max_length=100)
    team: str = Field(min_length=1, max_length=100)
    tool: str = Field(min_length=1, max_length=50)
    tokens: int = Field(gt=0)
    cost: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    used_on: date


class UsageRecordOut(BaseModel):
    # from_attributes lets Pydantic build this from a SQLAlchemy object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_name: str
    team: str
    tool: str
    tokens: int
    cost: Decimal
    used_on: date


class TeamSummary(BaseModel):
    """One row of GET /summary: totals for a single team."""

    model_config = ConfigDict(from_attributes=True)

    team: str
    total_tokens: int
    total_cost: Decimal
    record_count: int
