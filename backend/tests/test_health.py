import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_business_analyze_endpoint():
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Textile & Clothing",
        "available_capital": 100000.0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["financial"]["project_cost"] == 1000000.0
    assert data["financial"]["max_loan_amount"] == 900000.0
    assert data["scheme"]["scheme_name"] == "Term Loan Scheme"
    assert data["scheme"]["interest_rate_percent"] == 8.0
    assert data["scheme"]["tenure_years"] == 7
    assert data["scheme"]["moratorium_months"] == 6
    assert data["market"]["is_demo_data"] is True
    assert "disclaimer" in data
