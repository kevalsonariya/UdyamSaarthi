import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ==============================================================================
# 1. POST /financial/calculate TESTS
# ==============================================================================

def test_api_financial_calculate_valid_micro():
    """Test /financial/calculate with ₹10,000 margin."""
    payload = {"available_margin": 10000.0}
    response = client.post("/financial/calculate", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]
    assert data["project_cost"] == 100000.0
    assert data["maximum_loan"] == 90000.0
    assert data["scheme"] == "Micro Finance Scheme"
    assert data["interest_rate"] == 6.5
    assert data["tenure_years"] == 3
    assert data["moratorium_months"] == 3
    assert data["eligible_funding"] == 90000.0


def test_api_financial_calculate_boundary_14000():
    """Test /financial/calculate with ₹14,000 margin -> Micro Finance Scheme."""
    payload = {"available_margin": 14000.0}
    response = client.post("/financial/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["project_cost"] == 140000.0
    assert data["scheme"] == "Micro Finance Scheme"
    assert data["maximum_loan"] == 126000.0
    assert data["eligible_funding"] == 125000.0  # Capped at ₹1.25 Lakh


def test_api_financial_calculate_boundary_14001():
    """Test /financial/calculate with ₹14,001 margin -> Term Loan Scheme."""
    payload = {"available_margin": 14001.0}
    response = client.post("/financial/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["project_cost"] == 140010.0
    assert data["scheme"] == "Term Loan Scheme"
    assert data["interest_rate"] == 8.0
    assert data["tenure_years"] == 7
    assert data["moratorium_months"] == 6


def test_api_financial_calculate_invalid_margin():
    """Test /financial/calculate with negative margin -> 400 structured error."""
    payload = {"available_margin": -1000.0}
    response = client.post("/financial/calculate", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert "error" in json_data
    assert json_data["error"]["code"] == "VALUE_TOO_LOW"


def test_api_financial_calculate_exceeding_max_ceiling():
    """Test /financial/calculate with margin > ₹5 Lakh (project cost > ₹50 Lakh)."""
    payload = {"available_margin": 600000.0}
    response = client.post("/financial/calculate", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "EXCEEDS_MAX_PROJECT_COST"


# ==============================================================================
# 2. POST /scheme/recommend TESTS
# ==============================================================================

def test_api_scheme_recommend_micro():
    """Test /scheme/recommend with project cost <= ₹1.40 Lakh."""
    payload = {"project_cost": 120000.0}
    response = client.post("/scheme/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["scheme_name"] == "Micro Finance Scheme"
    assert data["interest_rate_percent"] == 6.5
    assert data["tenure_years"] == 3
    assert data["moratorium_months"] == 3
    assert data["maximum_agency_funding"] == 125000.0


def test_api_scheme_recommend_term():
    """Test /scheme/recommend with project cost > ₹1.40 Lakh."""
    payload = {"project_cost": 1000000.0}
    response = client.post("/scheme/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["scheme_name"] == "Term Loan Scheme"
    assert data["interest_rate_percent"] == 8.0
    assert data["tenure_years"] == 7
    assert data["moratorium_months"] == 6
    assert data["maximum_agency_funding"] == 4500000.0


def test_api_scheme_recommend_invalid():
    """Test /scheme/recommend with invalid cost > ₹50 Lakh."""
    payload = {"project_cost": 6000000.0}
    response = client.post("/scheme/recommend", json=payload)
    assert response.status_code == 400
    assert response.json()["success"] is False


# ==============================================================================
# 3. POST /emi/calculate TESTS
# ==============================================================================

def test_api_emi_calculate_direct():
    """Test /emi/calculate with direct loan parameters."""
    payload = {
        "principal": 90000.0,
        "annual_interest_rate": 6.5,
        "tenure_years": 3,
        "moratorium_months": 3,
    }
    response = client.post("/emi/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["principal"] == 90000.0
    assert data["monthly_emi"] == 2985.64
    assert data["moratorium_monthly_interest"] == 487.5
    assert data["post_moratorium_tenure_months"] == 33


def test_api_emi_calculate_from_margin():
    """Test /emi/calculate derived from available_margin."""
    payload = {"available_margin": 100000.0}
    response = client.post("/emi/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["principal"] == 900000.0
    assert data["monthly_emi"] == 14834.86


def test_api_emi_calculate_invalid():
    """Test /emi/calculate with invalid negative principal."""
    payload = {
        "principal": -5000.0,
        "annual_interest_rate": 6.5,
        "tenure_years": 3,
    }
    response = client.post("/emi/calculate", json=payload)
    assert response.status_code == 400
    assert response.json()["success"] is False


# ==============================================================================
# 4. POST /repayment/calculate TESTS
# ==============================================================================

def test_api_repayment_calculate():
    """Test /repayment/calculate schedule generation."""
    payload = {
        "principal": 90000.0,
        "annual_interest_rate": 6.5,
        "tenure_years": 3,
        "moratorium_months": 3,
    }
    response = client.post("/repayment/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    schedule = data["schedule"]
    assert len(schedule) == 36
    # Moratorium months
    assert schedule[0]["is_moratorium"] is True
    assert schedule[0]["principal"] == 0.0
    # Final month
    assert schedule[-1]["month"] == 36
    assert schedule[-1]["closing_balance"] == 0.0


# ==============================================================================
# 5. POST /working-capital/calculate TESTS
# ==============================================================================

def test_api_working_capital_calculate():
    """Test /working-capital/calculate endpoint."""
    payload = {
        "project_cost": 1000000.0,
        "monthly_emi": 14834.86,
    }
    response = client.post("/working-capital/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["monthly_raw_materials"] == 45000.0
    assert data["monthly_labor_wages"] == 25000.0
    assert data["total_monthly_operating_expense"] == 95000.0
    assert data["recommended_3_months_reserve"] == 285000.0
    assert data["break_even_occupancy_or_capacity_percent"] == 74.0


# ==============================================================================
# 6. PHASE B5 ENHANCEMENT API TESTS
# ==============================================================================

def test_api_repayment_calculate_with_quarterly_schedule():
    """Phase B5: Verify /repayment/calculate returns quarterly_schedule matching monthly sums."""
    payload = {
        "principal": 900000.0,
        "annual_interest_rate": 8.0,
        "tenure_years": 7,
        "moratorium_months": 6,
    }
    response = client.post("/repayment/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    # Verify both monthly schedule and quarterly schedule exist
    assert "schedule" in data
    assert "quarterly_schedule" in data
    assert len(data["schedule"]) == 84
    assert len(data["quarterly_schedule"]) == 28
    assert data["repayment_frequency"] == "Monthly (Quarterly roll-up available)"
    assert "indicative_notice" in data

    # Verify Quarter 1 and Quarter 2 are moratorium
    q1 = data["quarterly_schedule"][0]
    q2 = data["quarterly_schedule"][1]
    assert q1["is_moratorium"] is True
    assert q1["principal_paid"] == 0.0
    assert q2["is_moratorium"] is True
    assert q2["principal_paid"] == 0.0

    # Verify sum of quarter 1 payments equals sum of month 1..3 installments
    m1_3_pay = sum(data["schedule"][i]["installment_amount"] for i in range(3))
    assert q1["total_payment"] == round(m1_3_pay, 2)


def test_api_working_capital_calculate_phase_b5_breakdown():
    """Phase B5: Verify /working-capital/calculate returns itemized breakdown."""
    payload = {
        "project_cost": 1000000.0,
        "monthly_emi": 14834.86,
    }
    response = client.post("/working-capital/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    # All 10 requested fields
    assert data["monthly_operating_cost"] == 95000.0
    assert data["inventory"] == 45000.0
    assert data["utilities"] == 4000.0
    assert data["rent"] == 8000.0
    assert data["labour"] == 25000.0
    assert data["transportation"] == 8000.0
    assert data["marketing"] == 3000.0
    assert data["other"] == 2000.0
    assert data["recommended_reserve"] == 285000.0
    assert data["total_working_capital"] == 285000.0
    assert data["is_indicative_estimate"] is True

