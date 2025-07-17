from __future__ import annotations
import enum
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class RiskStatus(str, enum.Enum):
    """Overall workflow status for a risk."""
    IN_PROCESS = "in_process"
    COMPLETED = "completed"


class TaskStatus(str, enum.Enum):
    """Status for an individual task."""
    PENDING = "pending"
    COMPLETED = "completed"


class Risk(Base):
    """ORM model for an occupational risk entry."""
    __tablename__ = "risks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title:       Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category:    Mapped[str] = mapped_column(String, nullable=False)
    status:      Mapped[RiskStatus] = mapped_column(
        Enum(RiskStatus),
        default=RiskStatus.IN_PROCESS,
        nullable=False,
    )
    created_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="risk",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class Task(Base):
    """ORM model for a task assigned during the risk workflow."""
    __tablename__ = "tasks"

    id:         Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    risk_id:    Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("risks.id"),
        nullable=False,
    )
    assignee:   Mapped[str] = mapped_column(String, nullable=False)
    status:     Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    risk: Mapped[Risk] = relationship(
        "Risk",
        back_populates="tasks",
    )
