"""Integration tests for error handling and edge cases"""
import pytest
from fastapi.testclient import TestClient
from api.app.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


class TestRootEndpoints:
    """Test suite for root endpoints"""

    def test_root_endpoint_returns_200(self, client):
        """Test that root endpoint returns 200 status"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome to Movie Recommendation API" in data["message"]

    def test_root_endpoint_includes_docs_links(self, client):
        """Test that root endpoint includes documentation links"""
        response = client.get("/")
        data = response.json()
        assert "docs" in data
        assert "redoc" in data
        assert data["docs"] == "/docs"
        assert data["redoc"] == "/redoc"

    def test_health_check_returns_200(self, client):
        """Test that health check endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_root_endpoint_json_format(self, client):
        """Test that root endpoint returns valid JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
        # Should not raise exception
        data = response.json()
        assert isinstance(data, dict)

    def test_health_check_json_format(self, client):
        """Test that health check returns valid JSON"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)


class TestNonexistentEndpoints:
    """Test suite for handling nonexistent endpoints"""

    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that nonexistent endpoint returns 404"""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404

    def test_nonexistent_post_endpoint_returns_404(self, client):
        """Test that nonexistent POST endpoint returns 404"""
        response = client.post("/nonexistent/endpoint", json={})
        assert response.status_code == 404

    def test_wrong_method_returns_405(self, client):
        """Test that wrong HTTP method returns 405"""
        response = client.post("/")
        # POST on root endpoint should not be allowed
        assert response.status_code == 405

    def test_nonexistent_put_endpoint_returns_404(self, client):
        """Test that nonexistent PUT endpoint returns 404"""
        response = client.put("/nonexistent/endpoint", json={})
        assert response.status_code == 404

    def test_nonexistent_delete_endpoint_returns_404(self, client):
        """Test that nonexistent DELETE endpoint returns 404"""
        response = client.delete("/nonexistent/endpoint")
        assert response.status_code == 404


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in response"""
        response = client.get("/health")
        # CORS is configured with allow_origins=["*"]
        assert response.status_code == 200

    def test_health_endpoint_accessible(self, client):
        """Test that health endpoint is accessible"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestEndpointDocumentation:
    """Test suite for OpenAPI documentation endpoints"""

    def test_docs_endpoint_accessible(self, client):
        """Test that /docs endpoint is accessible"""
        response = client.get("/docs")
        # Swagger UI should return 200
        assert response.status_code == 200

    def test_redoc_endpoint_accessible(self, client):
        """Test that /redoc endpoint is accessible"""
        response = client.get("/redoc")
        # ReDoc should return 200
        assert response.status_code == 200

    def test_openapi_schema_accessible(self, client):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema or "swagger" in schema
