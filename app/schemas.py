from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .models import RiskStatus, TaskStatus


class TaskRead(BaseModel):
    id: UUID
    assignee: str
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = dict(from_attributes=True)


class RiskBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    category: str


class RiskCreate(RiskBase):
    """Request body for creating a new risk."""
    pass


class RiskRead(RiskBase):
    id: UUID
    status: RiskStatus
    created_at: datetime
    updated_at: datetime
    tasks: List[TaskRead] = []

    model_config = dict(from_attributes=True)
