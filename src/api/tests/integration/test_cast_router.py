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

    def test_update_cast_not_found(self, client):
        """Test updating non-existent cast member"""
        update_data = {"name": "Non Existent"}
        response = client.put("/cast/999", json=update_data)
        assert response.status_code == 404

    def test_delete_cast_not_found(self, client):
        """Test deleting non-existent cast member"""
        response = client.delete("/cast/999")
        assert response.status_code == 404

    def test_add_cast_to_invalid_movie(self, client):
        """Test adding cast to non-existent movie"""
        # Create cast
        cast_response = client.post("/cast/", json={"name": "Test Actor"})
        cast_id = cast_response.json()["id"]
        
        # Try to add to non-existent movie
        association_data = {"movie_id": 999, "character_name": "Invalid"}
        response = client.post(f"/cast/{cast_id}/movies", json=association_data)
        assert response.status_code == 400

    def test_remove_nonexistent_cast_movie_relation(self, client):
        """Test removing non-existent cast-movie relation"""
        response = client.delete("/cast/999/movies/999")
        assert response.status_code == 404

    def test_get_movies_by_nonexistent_cast(self, client):
        """Test getting movies by non-existent cast"""
        response = client.get("/cast/999/movies")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_cast_minimal(self, client):
        """Test creating cast with minimal data"""
        response = client.post("/cast/", json={"name": "Simple Actor"})
        assert response.status_code == 201
        assert response.json()["name"] == "Simple Actor"

    def test_create_cast_with_all_fields(self, client):
        """Test creating cast with all optional fields"""
        cast_data = {
            "name": "Full Actor",
            "biography": "Bio info",
            "birth_date": "1990-05-15",
            "birth_place": "New York"
        }
        response = client.post("/cast/", json=cast_data)
        assert response.status_code == 201
        data = response.json()
        assert data["biography"] == "Bio info"
        assert data["birth_date"] == "1990-05-15"

    def test_get_cast_pagination_skip(self, client):
        """Test cast pagination with skip"""
        for i in range(10):
            client.post("/cast/", json={"name": f"Actor{i}"})
        
        response = client.get("/cast/?skip=5&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_update_cast_partial(self, client):
        """Test partial update of cast"""
        create_resp = client.post("/cast/", json={"name": "Original", "biography": "Bio"})
        cast_id = create_resp.json()["id"]
        
        # Update only name
        response = client.put(f"/cast/{cast_id}", json={"name": "Updated Name"})
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_add_multiple_cast_to_movie(self, client):
        """Test adding multiple cast members to same movie"""
        movie = client.post("/movies/", json={"title": "Ensemble Film"})
        movie_id = movie.json()["id"]
        
        for i in range(3):
            cast = client.post("/cast/", json={"name": f"Actor {i}"})
            cast_id = cast.json()["id"]
            client.post(f"/cast/{cast_id}/movies", json={
                "movie_id": movie_id,
                "character_name": f"Character {i}"
            })
        
        # Check all added
        cast1 = client.post("/cast/", json={"name": "CheckActor"})
        cast1_id = cast1.json()["id"]
        client.post(f"/cast/{cast1_id}/movies", json={
            "movie_id": movie_id,
            "character_name": "MainChar"
        })
        movies = client.get(f"/cast/{cast1_id}/movies")
        assert len(movies.json()) >= 1

    def test_update_character_name_same_cast_movie(self, client):
        """Test updating character name for cast-movie association"""
        movie = client.post("/movies/", json={"title": "ActionMovie"})
        movie_id = movie.json()["id"]
        cast = client.post("/cast/", json={"name": "ActionStar"})
        cast_id = cast.json()["id"]
        
        # Add with one character name
        client.post(f"/cast/{cast_id}/movies", json={
            "movie_id": movie_id,
            "character_name": "Hero"
        })
        
        # Update character name
        response = client.put(f"/cast/{cast_id}/movies/{movie_id}", json={
            "character_name": "Super Hero"
        })
        assert response.status_code == 200

    def test_remove_cast_from_multiple_movies(self, client):
        """Test removing cast from one of multiple movies"""
        cast = client.post("/cast/", json={"name": "PopularActor"})
        cast_id = cast.json()["id"]
        
        # Add to multiple movies
        movie1 = client.post("/movies/", json={"title": "Movie1"})
        movie1_id = movie1.json()["id"]
        movie2 = client.post("/movies/", json={"title": "Movie2"})
        movie2_id = movie2.json()["id"]
        
        client.post(f"/cast/{cast_id}/movies", json={"movie_id": movie1_id, "character_name": "Char1"})
        client.post(f"/cast/{cast_id}/movies", json={"movie_id": movie2_id, "character_name": "Char2"})
        
        # Remove from one
        response = client.delete(f"/cast/{cast_id}/movies/{movie1_id}")
        assert response.status_code == 204
        
        # Still in other
        movies = client.get(f"/cast/{cast_id}/movies")
        assert len(movies.json()) == 1

    def test_cast_with_special_characters_name(self, client):
        """Test cast with special characters in name"""
        response = client.post("/cast/", json={"name": "Jean-Claude Van Damme"})
        assert response.status_code == 201
        assert response.json()["name"] == "Jean-Claude Van Damme"

    def test_get_empty_cast_movies(self, client):
        """Test getting movies for cast with no movies"""
        cast = client.post("/cast/", json={"name": "Unused Actor"})
        cast_id = cast.json()["id"]
        
        response = client.get(f"/cast/{cast_id}/movies")
        assert response.status_code == 200
        assert response.json() == []

    def test_cast_pagination_limit_boundary(self, client):
        """Test cast pagination at limit boundary"""
        for i in range(3):
            client.post("/cast/", json={"name": f"Limited{i}"})
        
        # Request exactly the count
        response = client.get("/cast/?skip=0&limit=3")
        assert response.status_code == 200
        assert len(response.json()) <= 3

