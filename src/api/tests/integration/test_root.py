"""
Simple test to verify pytest and conftest are working
"""


def test_conftest_fixture(client):
    """Test that client fixture is working"""
    assert client is not None


def test_root_endpoint(client):
    """Test that the root endpoint is accessible"""
    response = client.get("/")
    assert response.status_code == 200
