import asyncio
from uuid import UUID
from sqlalchemy.orm import Session

from .database import SessionLocal
from .crud import complete_risk_workflow, get_risk


async def simulate_workflow(risk_id: UUID) -> None:
    """Simulate a 10-second delay then complete the risk workflow."""
    await asyncio.sleep(10)
    db: Session = SessionLocal()
    try:
        risk = get_risk(db, risk_id)
        if risk:
            complete_risk_workflow(db, risk)
    finally:
        db.close()
