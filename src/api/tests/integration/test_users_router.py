class TestUsersRouter:
    """Integration tests for Users Router"""

    def test_create_user(self, client):
        """Test creating a new user"""
        user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "full_name": "John Doe"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "john_doe"
        assert data["email"] == "john@example.com"
        assert "password" not in data
        assert "hashed_password" not in data
        assert "id" in data

    def test_get_all_users(self, client):
        """Test getting all users"""
        client.post("/users/", json={"username": "user1", "email": "user1@test.com", "password": "pass123"})
        client.post("/users/", json={"username": "user2", "email": "user2@test.com", "password": "pass456"})
        
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_user_by_id(self, client):
        """Test getting a specific user by ID"""
        create_response = client.post("/users/", json={
            "username": "jane_doe",
            "email": "jane@example.com",
            "password": "password123"
        })
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "jane_doe"

    def test_get_user_not_found(self, client):
        """Test getting a non-existent user"""
        response = client.get("/users/999")
        assert response.status_code == 404

    def test_update_user(self, client):
        """Test updating a user"""
        create_response = client.post("/users/", json={
            "username": "updateme",
            "email": "update@example.com",
            "password": "oldpass"
        })
        user_id = create_response.json()["id"]
        
        update_data = {"full_name": "Updated Name", "bio": "New bio"}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["bio"] == "New bio"

    def test_delete_user(self, client):
        """Test deleting a user"""
        create_response = client.post("/users/", json={
            "username": "deleteme",
            "email": "delete@example.com",
            "password": "pass123"
        })
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_create_user_duplicate_username(self, client):
        """Test creating user with duplicate username"""
        user_data = {"username": "duplicate", "email": "user1@test.com", "password": "pass123"}
        client.post("/users/", json=user_data)
        
        # Try to create with same username but different email
        duplicate_data = {"username": "duplicate", "email": "user2@test.com", "password": "pass456"}
        response = client.post("/users/", json=duplicate_data)
        assert response.status_code == 400

    def test_create_user_duplicate_email(self, client):
        """Test creating user with duplicate email"""
        user_data = {"username": "user1", "email": "duplicate@test.com", "password": "pass123"}
        client.post("/users/", json=user_data)
        
        # Try to create with same email but different username
        duplicate_data = {"username": "user2", "email": "duplicate@test.com", "password": "pass456"}
        response = client.post("/users/", json=duplicate_data)
        assert response.status_code == 400

    def test_update_user_not_found(self, client):
        """Test updating non-existent user"""
        response = client.put("/users/999", json={"full_name": "Test"})
        assert response.status_code == 404

    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user"""
        response = client.delete("/users/999")
        assert response.status_code == 404

    def test_get_all_users_empty(self, client):
        """Test getting all users when none exist"""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_user_missing_email(self, client):
        """Test creating user without email"""
        user_data = {"username": "nomail", "password": "pass123"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422

    def test_create_user_invalid_email(self, client):
        """Test creating user with invalid email format"""
        user_data = {"username": "bademail", "email": "not-an-email", "password": "pass123"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422

    def test_create_user_missing_password(self, client):
        """Test creating user without password"""
        user_data = {"username": "nopass", "email": "test@example.com"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422

    def test_update_user_email_exists(self, client):
        """Test updating user email to one that already exists"""
        # Create two users
        user1 = client.post("/users/", json={"username": "user1", "email": "email1@test.com", "password": "pass"})
        user1_id = user1.json()["id"]
        user2 = client.post("/users/", json={"username": "user2", "email": "email2@test.com", "password": "pass"})
        
        # Try to update user1's email to user2's email
        response = client.put(f"/users/{user1_id}", json={"email": "email2@test.com"})
        assert response.status_code == 400
