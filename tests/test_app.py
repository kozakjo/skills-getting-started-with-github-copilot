import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    activity = "Basketball"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400  # Already signed up is 400
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200 or response.status_code == 404  # Not found is 404

def test_signup_duplicate():
    activity = "Tennis Club"
    email = "sarah@mergington.edu"  # Already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_unregister_not_found():
    activity = "Art Studio"
    email = "notfound@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
