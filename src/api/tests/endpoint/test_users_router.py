"""Fixed integration tests for Users Router"""


class TestUsersRouter:
    """Integration tests for Users Router"""

    def test_create_user(self, client):
        """Test creating a user"""
        user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "secure_password"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "john_doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    def test_create_user_with_name(self, client):
        """Test creating a user with name"""
        user_data = {
            "username": "jane_doe",
            "email": "jane@example.com",
            "password": "secure_password",
            "name": "Jane Doe"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Jane Doe"

    def test_get_user_by_id(self, client):
        """Test getting a specific user"""
        create_response = client.post("/users/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password"
        })
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    def test_get_user_not_found(self, client):
        """Test getting non-existent user"""
        response = client.get("/users/999")
        assert response.status_code == 404

    def test_update_user(self, client):
        """Test updating a user"""
        create_response = client.post("/users/register", json={
            "username": "olduser",
            "email": "old@example.com",
            "password": "password"
        })
        user_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated Name",
            "email": "newemail@example.com"
        }
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_user(self, client):
        """Test deleting a user"""
        create_response = client.post("/users/register", json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "password": "password"
        })
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404

    def test_create_user_duplicate_username(self, client):
        """Test creating user with duplicate username"""
        user_data = {
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password"
        }
        client.post("/users/register", json=user_data)
        
        duplicate_data = {
            "username": "duplicate",
            "email": "second@example.com",
            "password": "password"
        }
        response = client.post("/users/register", json=duplicate_data)
        assert response.status_code in [400, 409]  # Bad request or conflict

    def test_create_user_missing_email(self, client):
        """Test creating user without email"""
        user_data = {
            "username": "noemail",
            "password": "password"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code in [400, 422]  # Validation error

    def test_create_user_missing_password(self, client):
        """Test creating user without password"""
        user_data = {
            "username": "nopass",
            "email": "nopass@example.com"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code in [400, 422]  # Validation error

    def test_login_user(self, client):
        """Test user login"""
        # First register a user
        client.post("/users/register", json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123"
        })
        
        # Then login
        login_data = {
            "username": "loginuser",
            "password": "password123"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
