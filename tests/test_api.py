import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_page_renders_ssr():
    """Ensure the Server-Side Rendered login page is reachable and valid."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "Sign In" in response.text
    assert "CashFlow Pro" in response.text

def test_unauthorized_dashboard_redirect():
    """Ensure non-authenticated users hitting the dashboard are redirected to login."""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"

def test_api_security_enforcement():
    """Ensure raw JSON endpoints cleanly reject unauthorized requests with a 401."""
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_api_validation_rejection():
    """Ensure missing request bodies trigger standard 422 HTTP validation errors."""
    response = client.post("/api/users/register", json={})
    assert response.status_code == 422
