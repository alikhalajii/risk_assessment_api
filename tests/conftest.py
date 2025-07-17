import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
import app.workflow as workflow_mod
import app.main as main_mod

# Set up an in-memory SQLite database with StaticPool so that
# the same connection is shared across threads.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)

# Create all tables once
Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def configure_app():
    """
    Configure the FastAPI app for testing:
      - Override get_db() to use the in-memory database.
      - Stub out simulate_workflow to skip the delay and completion logic.
    """
    # Override the DB dependency to use our in-memory session
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db

    # Replace the background workflow with a no-op
    def no_workflow(risk_id):
        return None
    workflow_mod.simulate_workflow = no_workflow
    main_mod.simulate_workflow = no_workflow

    yield

    # Clean up overrides after each test
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app."""
    return TestClient(app)
