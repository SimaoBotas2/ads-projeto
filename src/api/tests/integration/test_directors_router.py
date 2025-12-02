"""Fixed integration tests for Directors Router"""


class TestDirectorsRouter:
    """Integration tests for Directors Router"""

    def test_get_all_directors_empty(self, client):
        """Test getting all directors when database is empty"""
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_director(self, client):
        """Test creating a director"""
        director_data = {"name": "Steven Spielberg"}
        response = client.post("/directors/", json=director_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Steven Spielberg"
        assert "id" in data

    def test_create_director_with_nacionality(self, client):
        """Test creating a director with nacionality"""
        director_data = {"name": "Christopher Nolan", "nacionality": "British"}
        response = client.post("/directors/", json=director_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Christopher Nolan"
        assert data["nacionality"] == "British"

    def test_get_all_directors(self, client):
        """Test getting all directors"""
        client.post("/directors/", json={"name": "Director 1"})
        client.post("/directors/", json={"name": "Director 2"})
        
        response = client.get("/directors/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_director_by_id(self, client):
        """Test getting a specific director"""
        create_response = client.post("/directors/", json={"name": "James Cameron"})
        director_id = create_response.json()["id"]
        
        response = client.get(f"/directors/{director_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "James Cameron"

    def test_get_director_not_found(self, client):
        """Test getting non-existent director"""
        response = client.get("/directors/999")
        assert response.status_code == 404

    def test_update_director(self, client):
        """Test updating a director"""
        create_response = client.post("/directors/", json={"name": "Old Name"})
        director_id = create_response.json()["id"]
        
        update_data = {"name": "New Name", "nacionality": "American"}
        response = client.put(f"/directors/{director_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"

    def test_delete_director(self, client):
        """Test deleting a director"""
        create_response = client.post("/directors/", json={"name": "Director to Delete"})
        director_id = create_response.json()["id"]
        
        response = client.delete(f"/directors/{director_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/directors/{director_id}")
        assert response.status_code == 404
