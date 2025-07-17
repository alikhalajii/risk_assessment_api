from uuid import UUID
from fastapi.testclient import TestClient

# Sample payload for creating a risk
RISK_PAYLOAD = {
    "title": "Lärmbelastung",
    "description": "Der Schallpegel überschreitet die Grenze von 90 dB.",
    "category": "Physikalisch",
}


def test_create_risk_success(client: TestClient):
    """
    When POST /risks is called with valid data,
    it should return 201 Created, status 'in_process',
    and exactly two automatically generated tasks.
    """
    response = client.post("/risks", json=RISK_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    # The response must include an 'id'
    assert "id" in data
    # Initial workflow state is 'in_process'
    assert data["status"] == "in_process"
    # Two default tasks should be present
    assert isinstance(data["tasks"], list) and len(data["tasks"]) == 2


def test_create_risk_conflict(client: TestClient):
    """
    Posting the same payload a second time
    should return 409 Conflict to prevent duplicates.
    """
    response = client.post("/risks", json=RISK_PAYLOAD)
    assert response.status_code == 409


def test_list_and_get_in_process(client: TestClient):
    """
    GET /risks should return a list containing at least one risk.
    GET /risks/{id} for that risk should show status 'in_process'.
    """
    # List all risks
    list_response = client.get("/risks")
    assert list_response.status_code == 200
    risks = list_response.json()
    assert isinstance(risks, list) and len(risks) >= 1

    # Fetch the first risk by its UUID
    first_id = UUID(risks[0]["id"])
    detail_response = client.get(f"/risks/{first_id}")
    assert detail_response.status_code == 200
    # Confirm it's still in 'in_process' state
    assert detail_response.json()["status"] == "in_process"
