from datetime import datetime, timezone
import uuid

from fastapi import HTTPException, status
from sqlalchemy import exists
from sqlalchemy.orm import Session

from . import models, schemas


def create_risk(db: Session, risk_in: schemas.RiskCreate) -> models.Risk:
    """Insert a new risk and two default tasks; 409 on duplicate title."""
    if db.query(exists().where(models.Risk.title == risk_in.title)).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A risk with this title already exists.",
        )
    risk = models.Risk(
        title=risk_in.title,
        description=risk_in.description,
        category=risk_in.category,
    )
    db.add(risk)
    db.flush()  # assigns risk.id
    for assignee in ("Sicherheitsbeauftragter", "Teamleiter"):
        db.add(models.Task(risk_id=risk.id, assignee=assignee))
    db.commit()
    db.refresh(risk)
    return risk


def get_risks(db: Session):
    """Return all risks with their tasks."""
    return db.query(models.Risk).all()


def get_risk(db: Session, risk_id: uuid.UUID):
    """Return a single risk by UUID or None."""
    return db.query(models.Risk).filter(models.Risk.id == risk_id).first()


def complete_risk_workflow(db: Session, risk: models.Risk) -> models.Risk:
    """Mark risk and its tasks as completed with UTC timestamp."""
    now = datetime.now(timezone.utc)
    for task in risk.tasks:
        task.status = models.TaskStatus.COMPLETED
        task.completed_at = now
    risk.status = models.RiskStatus.COMPLETED
    db.commit()
    db.refresh(risk)
    return risk
