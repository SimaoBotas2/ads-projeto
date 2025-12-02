"""Fixed integration tests for Cast Router - uses actual model fields"""


class TestCastRouter:
    """Integration tests for Cast Router"""

    def test_get_all_cast_empty(self, client):
        """Test getting all cast when database is empty"""
        response = client.get("/cast/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_cast_minimal(self, client):
        """Test creating a cast member with minimal fields"""
        cast_data = {"name": "Leonardo DiCaprio"}
        response = client.post("/cast/", json=cast_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Leonardo DiCaprio"
        assert "id" in data

    def test_create_cast_with_nacionality(self, client):
        """Test creating a cast member with all available fields"""
        cast_data = {
            "name": "Tom Hanks",
            "nacionality": "American"
        }
        response = client.post("/cast/", json=cast_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tom Hanks"
        assert data["nacionality"] == "American"

    def test_get_all_cast(self, client):
        """Test getting all cast members"""
        client.post("/cast/", json={"name": "Tom Hanks"})
        client.post("/cast/", json={"name": "Meryl Streep"})
        
        response = client.get("/cast/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_cast_by_id(self, client):
        """Test getting a specific cast member by ID"""
        create_response = client.post("/cast/", json={"name": "Brad Pitt"})
        cast_id = create_response.json()["id"]
        
        response = client.get(f"/cast/{cast_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cast_id
        assert data["name"] == "Brad Pitt"

    def test_get_cast_not_found(self, client):
        """Test getting a non-existent cast member"""
        response = client.get("/cast/999")
        assert response.status_code == 404

    def test_update_cast(self, client):
        """Test updating a cast member"""
        create_response = client.post("/cast/", json={"name": "Julia Roberts"})
        cast_id = create_response.json()["id"]
        
        update_data = {"name": "Julia Roberts", "nacionality": "American"}
        response = client.put(f"/cast/{cast_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nacionality"] == "American"

    def test_delete_cast(self, client):
        """Test deleting a cast member"""
        create_response = client.post("/cast/", json={"name": "Will Smith"})
        cast_id = create_response.json()["id"]
        
        response = client.delete(f"/cast/{cast_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = client.get(f"/cast/{cast_id}")
        assert response.status_code == 404

    def test_get_cast_with_pagination(self, client):
        """Test getting cast with pagination"""
        for i in range(5):
            client.post("/cast/", json={"name": f"Actor {i}"})
        
        response = client.get("/cast/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

