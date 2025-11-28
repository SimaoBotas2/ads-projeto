from datetime import date


class TestGenresRouter:
    """Integration tests for Genres Router"""

    def test_get_all_genres_empty(self, client):
        """Test getting all genres when database is empty"""
        response = client.get("/genres/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_genre(self, client):
        """Test creating a new genre"""
        genre_data = {
            "name": "Action",
            "description": "Action movies with explosions"
        }
        response = client.post("/genres/", json=genre_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Action"
        assert data["description"] == "Action movies with explosions"
        assert "id" in data

    def test_get_all_genres(self, client):
        """Test getting all genres after creating some"""
        # Create genres
        client.post("/genres/", json={"name": "Action", "description": "Action movies"})
        client.post("/genres/", json={"name": "Drama", "description": "Drama movies"})
        
        response = client.get("/genres/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Action"
        assert data[1]["name"] == "Drama"

    def test_get_genre_by_id(self, client):
        """Test getting a specific genre by ID"""
        # Create genre
        create_response = client.post("/genres/", json={"name": "Comedy"})
        genre_id = create_response.json()["id"]
        
        response = client.get(f"/genres/{genre_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == genre_id
        assert data["name"] == "Comedy"

    def test_get_genre_not_found(self, client):
        """Test getting a non-existent genre"""
        response = client.get("/genres/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Genre not found"

    def test_update_genre(self, client):
        """Test updating a genre"""
        # Create genre
        create_response = client.post("/genres/", json={"name": "Sci-Fi"})
        genre_id = create_response.json()["id"]
        
        # Update genre
        update_data = {"name": "Science Fiction", "description": "Futuristic movies"}
        response = client.put(f"/genres/{genre_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Science Fiction"
        assert data["description"] == "Futuristic movies"

    def test_update_genre_not_found(self, client):
        """Test updating a non-existent genre"""
        response = client.put("/genres/999", json={"name": "Updated"})
        assert response.status_code == 404

    def test_delete_genre(self, client):
        """Test deleting a genre"""
        # Create genre
        create_response = client.post("/genres/", json={"name": "Horror"})
        genre_id = create_response.json()["id"]
        
        # Delete genre
        response = client.delete(f"/genres/{genre_id}")
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/genres/{genre_id}")
        assert get_response.status_code == 404

    def test_delete_genre_not_found(self, client):
        """Test deleting a non-existent genre"""
        response = client.delete("/genres/999")
        assert response.status_code == 404
