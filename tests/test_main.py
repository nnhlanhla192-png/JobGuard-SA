from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_home_endpoint_returns_running_status():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["application"] == "JobGuard SA"
    assert data["status"] == "running"


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_job_checker_flags_upfront_fee_and_guaranteed_job():
    response = client.post(
        "/check-job",
        json={
            "job_text": "Pay a registration fee to get a guaranteed job. No interview required."
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "High"
    assert len(data["warning_signs"]) >= 2
    assert any("registration fee" in warning for warning in data["warning_signs"])
    assert any("guaranteed job" in warning for warning in data["warning_signs"])
    assert data["advice"]


def test_job_checker_returns_uncertain_when_no_known_phrases_match():
    response = client.post(
        "/check-job",
        json={
            "job_text": "We are recruiting a junior administrator. Submit your CV by Friday."
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "Uncertain"
    assert data["warning_signs"] == []
    assert "does not prove" in data["advice"]


def test_job_checker_rejects_text_that_is_too_short():
    response = client.post("/check-job", json={"job_text": "scam"})

    assert response.status_code == 422


def test_job_checker_rejects_missing_job_text():
    response = client.post("/check-job", json={})

    assert response.status_code == 422