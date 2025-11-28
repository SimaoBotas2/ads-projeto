from datetime import date


class TestCastRouter:
    """Integration tests for Cast Router"""

    def test_get_all_cast_empty(self, client):
        """Test getting all cast when database is empty"""
        response = client.get("/cast/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_cast(self, client):
        """Test creating a new cast member"""
        cast_data = {
            "name": "Leonardo DiCaprio",
            "biography": "American actor",
            "birth_date": "1974-11-11",
            "birth_place": "Los Angeles, California"
        }
        response = client.post("/cast/", json=cast_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Leonardo DiCaprio"
        assert data["birth_date"] == "1974-11-11"
        assert "id" in data

    def test_get_all_cast(self, client):
        """Test getting all cast members"""
        client.post("/cast/", json={"name": "Tom Hanks"})
        client.post("/cast/", json={"name": "Meryl Streep"})
        
        response = client.get("/cast/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_cast_with_pagination(self, client):
        """Test getting cast with pagination"""
        for i in range(5):
            client.post("/cast/", json={"name": f"Actor {i}"})
        
        response = client.get("/cast/?skip=2&limit=2")
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
        create_response = client.post("/cast/", json={"name": "Robert De Niro"})
        cast_id = create_response.json()["id"]
        
        update_data = {"name": "Robert Anthony De Niro", "biography": "American actor"}
        response = client.put(f"/cast/{cast_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Robert Anthony De Niro"
        assert data["biography"] == "American actor"

    def test_delete_cast(self, client):
        """Test deleting a cast member"""
        create_response = client.post("/cast/", json={"name": "Al Pacino"})
        cast_id = create_response.json()["id"]
        
        response = client.delete(f"/cast/{cast_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/cast/{cast_id}")
        assert get_response.status_code == 404

    def test_add_cast_to_movie(self, client):
        """Test adding a cast member to a movie"""
        # Create movie
        movie_response = client.post("/movies/", json={"title": "Inception"})
        movie_id = movie_response.json()["id"]
        
        # Create cast
        cast_response = client.post("/cast/", json={"name": "Leonardo DiCaprio"})
        cast_id = cast_response.json()["id"]
        
        # Add cast to movie
        association_data = {"movie_id": movie_id, "character_name": "Dom Cobb"}
        response = client.post(f"/cast/{cast_id}/movies", json=association_data)
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Cast member added to movie successfully"

    def test_get_movies_by_cast(self, client):
        """Test getting movies by cast member"""
        # Create movie and cast
        movie_response = client.post("/movies/", json={"title": "The Matrix"})
        movie_id = movie_response.json()["id"]
        cast_response = client.post("/cast/", json={"name": "Keanu Reeves"})
        cast_id = cast_response.json()["id"]
        
        # Add cast to movie
        client.post(f"/cast/{cast_id}/movies", json={"movie_id": movie_id, "character_name": "Neo"})
        
        # Get movies by cast
        response = client.get(f"/cast/{cast_id}/movies")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["movie_title"] == "The Matrix"
        assert data[0]["character_name"] == "Neo"

    def test_update_character_name(self, client):
        """Test updating character name for cast-movie association"""
        # Create and associate
        movie_response = client.post("/movies/", json={"title": "Pulp Fiction"})
        movie_id = movie_response.json()["id"]
        cast_response = client.post("/cast/", json={"name": "John Travolta"})
        cast_id = cast_response.json()["id"]
        client.post(f"/cast/{cast_id}/movies", json={"movie_id": movie_id, "character_name": "Vincent"})
        
        # Update character name
        response = client.put(f"/cast/{cast_id}/movies/{movie_id}", json={"character_name": "Vincent Vega"})
        assert response.status_code == 200
        assert response.json()["message"] == "Character name updated successfully"

    def test_remove_cast_from_movie(self, client):
        """Test removing cast from movie"""
        # Create and associate
        movie_response = client.post("/movies/", json={"title": "Fight Club"})
        movie_id = movie_response.json()["id"]
        cast_response = client.post("/cast/", json={"name": "Edward Norton"})
        cast_id = cast_response.json()["id"]
        client.post(f"/cast/{cast_id}/movies", json={"movie_id": movie_id, "character_name": "Narrator"})
        
        # Remove association
        response = client.delete(f"/cast/{cast_id}/movies/{movie_id}")
        assert response.status_code == 204
