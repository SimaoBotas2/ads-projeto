from datetime import date


class TestDirectorsRouter:
    """Integration tests for Directors Router"""

    def test_get_all_directors_empty(self, client):
        """Test getting all directors when database is empty"""
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_director(self, client):
        """Test creating a new director"""
        director_data = {
            "name": "Christopher Nolan",
            "biography": "British-American filmmaker",
            "birth_date": "1970-07-30",
            "birth_place": "London, England"
        }
        response = client.post("/directors/", json=director_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Christopher Nolan"
        assert data["biography"] == "British-American filmmaker"
        assert data["birth_date"] == "1970-07-30"
        assert "id" in data

    def test_get_all_directors(self, client):
        """Test getting all directors"""
        client.post("/directors/", json={"name": "Steven Spielberg"})
        client.post("/directors/", json={"name": "Martin Scorsese"})
        
        response = client.get("/directors/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_director_by_id(self, client):
        """Test getting a specific director by ID"""
        create_response = client.post("/directors/", json={"name": "Quentin Tarantino"})
        director_id = create_response.json()["id"]
        
        response = client.get(f"/directors/{director_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == director_id
        assert data["name"] == "Quentin Tarantino"

    def test_get_director_not_found(self, client):
        """Test getting a non-existent director"""
        response = client.get("/directors/999")
        assert response.status_code == 404

    def test_update_director(self, client):
        """Test updating a director"""
        create_response = client.post("/directors/", json={"name": "James Cameron"})
        director_id = create_response.json()["id"]
        
        update_data = {"name": "James Francis Cameron", "biography": "Canadian filmmaker"}
        response = client.put(f"/directors/{director_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "James Francis Cameron"
        assert data["biography"] == "Canadian filmmaker"

    def test_delete_director(self, client):
        """Test deleting a director"""
        create_response = client.post("/directors/", json={"name": "David Fincher"})
        director_id = create_response.json()["id"]
        
        response = client.delete(f"/directors/{director_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/directors/{director_id}")
        assert get_response.status_code == 404

    def test_update_director_not_found(self, client):
        """Test updating non-existent director"""
        response = client.put("/directors/999", json={"name": "Test"})
        assert response.status_code == 404

    def test_delete_director_not_found(self, client):
        """Test deleting non-existent director"""
        response = client.delete("/directors/999")
        assert response.status_code == 404

    def test_get_all_directors_with_pagination(self, client):
        """Test getting directors with pagination"""
        for i in range(5):
            client.post("/directors/", json={"name": f"Director {i}"})
        
        response = client.get("/directors/?skip=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
