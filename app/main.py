from typing import List
from uuid import UUID

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db
from .workflow import simulate_workflow

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Risk Assessment Workflow API",
    version="1.0.0",
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Risk API. See /docs for usage."}


@app.post(
    "/risks",
    response_model=schemas.RiskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_risk_endpoint(
    risk_in: schemas.RiskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Endpoint to create a risk and start the workflow."""
    risk = crud.create_risk(db, risk_in)
    background_tasks.add_task(simulate_workflow, risk.id)
    return risk


@app.get("/risks", response_model=List[schemas.RiskRead])
async def list_risks_endpoint(db: Session = Depends(get_db)):
    """List all risks with their tasks."""
    return crud.get_risks(db)


@app.get("/risks/{risk_id}", response_model=schemas.RiskRead)
async def get_risk_endpoint(
    risk_id: UUID,
    db: Session = Depends(get_db),
):
    """Get details of one risk or return 404 if not found."""
    risk = crud.get_risk(db, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk
