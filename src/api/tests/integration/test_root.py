"""Fixed integration tests for root and health endpoints"""


class TestRootEndpoints:
    """Test root and health endpoints"""

    def test_root_endpoint_returns_200(self, client):
        """Test that root endpoint returns 200 status"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]

    def test_health_check_returns_200(self, client):
        """Test that health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
