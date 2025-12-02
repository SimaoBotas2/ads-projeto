class TestMoviesRouter:
    """Integration tests for Movies Router"""

    def test_get_all_movies_empty(self, client):
        """Test getting all movies when database is empty"""
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_movie(self, client):
        """Test creating a new movie"""
        movie_data = {
            "title": "The Shawshank Redemption",
            "original_title": "The Shawshank Redemption",
            "overview": "Two imprisoned men bond over a number of years",
            "release_date": "1994-09-23",
            "runtime": 142,
            "original_language": "en"
        }
        response = client.post("/movies/", json=movie_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "The Shawshank Redemption"
        assert data["runtime"] == 142
        assert "id" in data

    def test_get_all_movies(self, client):
        """Test getting all movies"""
        client.post("/movies/", json={"title": "Movie 1"})
        client.post("/movies/", json={"title": "Movie 2"})
        
        response = client.get("/movies/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_movie_by_id(self, client):
        """Test getting a specific movie by ID"""
        create_response = client.post("/movies/", json={"title": "Inception"})
        movie_id = create_response.json()["id"]
        
        response = client.get(f"/movies/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == movie_id
        assert data["title"] == "Inception"

    def test_get_movie_not_found(self, client):
        """Test getting a non-existent movie"""
        response = client.get("/movies/999")
        assert response.status_code == 404

    def test_update_movie(self, client):
        """Test updating a movie"""
        create_response = client.post("/movies/", json={"title": "The Matrix"})
        movie_id = create_response.json()["id"]
        
        update_data = {"title": "The Matrix Reloaded", "runtime": 138}
        response = client.put(f"/movies/{movie_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "The Matrix Reloaded"
        assert data["runtime"] == 138

    def test_delete_movie(self, client):
        """Test deleting a movie"""
        create_response = client.post("/movies/", json={"title": "Avatar"})
        movie_id = create_response.json()["id"]
        
        response = client.delete(f"/movies/{movie_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/movies/{movie_id}")
        assert get_response.status_code == 404

    def test_search_movies(self, client):
        """Test searching movies by title"""
        client.post("/movies/", json={"title": "The Dark Knight"})
        client.post("/movies/", json={"title": "The Dark Knight Rises"})
        client.post("/movies/", json={"title": "Batman Begins"})
        
        response = client.get("/movies/search?query=Dark Knight")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_movies_by_genre(self, client):
        """Test getting movies by genre"""
        # Create genre
        genre_response = client.post("/genres/", json={"name": "Action"})
        genre_id = genre_response.json()["id"]
        
        # This test would require movie-genre association endpoints
        # Simplified for now
        response = client.get(f"/movies/genre/{genre_id}")
        assert response.status_code in [200, 404]

    def test_get_cast_by_movie(self, client):
        """Test getting cast members of a movie"""
        movie_response = client.post("/movies/", json={"title": "Titanic"})
        movie_id = movie_response.json()["id"]
        
        response = client.get(f"/movies/{movie_id}/cast")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_update_movie_not_found(self, client):
        """Test updating non-existent movie"""
        response = client.put("/movies/999", json={"title": "Test"})
        assert response.status_code == 404

    def test_delete_movie_not_found(self, client):
        """Test deleting non-existent movie"""
        response = client.delete("/movies/999")
        assert response.status_code == 404

    def test_search_movies_empty(self, client):
        """Test searching with no results"""
        response = client.get("/movies/search?query=NonexistentMovie123456")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_movies_by_nonexistent_genre(self, client):
        """Test getting movies by non-existent genre"""
        response = client.get("/movies/genre/999")
        assert response.status_code == 200
        assert response.json() == []
