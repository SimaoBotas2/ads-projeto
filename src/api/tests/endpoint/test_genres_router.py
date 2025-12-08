"""Fixed integration tests for Genres Router"""


class TestGenresRouter:
    """Integration tests for Genres Router"""

    def test_get_all_genres_empty(self, client):
        """Test getting all genres when database is empty"""
        response = client.get("/genres/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_genre(self, client):
        """Test creating a genre"""
        genre_data = {"name": "Action"}
        response = client.post("/genres/", json=genre_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Action"
        assert "id" in data

    def test_get_all_genres(self, client):
        """Test getting all genres"""
        client.post("/genres/", json={"name": "Drama"})
        client.post("/genres/", json={"name": "Comedy"})
        
        response = client.get("/genres/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_genre_by_id(self, client):
        """Test getting a specific genre"""
        create_response = client.post("/genres/", json={"name": "Thriller"})
        genre_id = create_response.json()["id"]
        
        response = client.get(f"/genres/{genre_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Thriller"

    def test_get_genre_not_found(self, client):
        """Test getting non-existent genre"""
        response = client.get("/genres/999")
        assert response.status_code == 404

    def test_update_genre(self, client):
        """Test updating a genre"""
        create_response = client.post("/genres/", json={"name": "SciFi"})
        genre_id = create_response.json()["id"]
        
        update_data = {"name": "Science Fiction"}
        response = client.put(f"/genres/{genre_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Science Fiction"

    def test_delete_genre(self, client):
        """Test deleting a genre"""
        create_response = client.post("/genres/", json={"name": "Horror"})
        genre_id = create_response.json()["id"]
        
        response = client.delete(f"/genres/{genre_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/genres/{genre_id}")
        assert response.status_code == 404
