class TestRatingsRouter:
    """Integration tests for Ratings Router"""

    def test_create_rating(self, client):
        """Test creating a new rating"""
        # Create user and movie first
        user_response = client.post("/users/", json={
            "username": "rater",
            "email": "rater@test.com",
            "password": "pass123"
        })
        user_id = user_response.json()["id"]
        
        movie_response = client.post("/movies/", json={"title": "Interstellar"})
        movie_id = movie_response.json()["id"]
        
        # Create rating
        rating_data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": 9.5,
            "review": "Amazing movie!"
        }
        response = client.post("/ratings/", json=rating_data)
        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 9.5
        assert data["review"] == "Amazing movie!"
        assert "id" in data

    def test_get_all_ratings(self, client):
        """Test getting all ratings"""
        # Setup
        user = client.post("/users/", json={"username": "user1", "email": "u1@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Movie 1"})
        
        client.post("/ratings/", json={
            "user_id": user.json()["id"],
            "movie_id": movie.json()["id"],
            "rating": 8.0
        })
        
        response = client.get("/ratings/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_rating_by_id(self, client):
        """Test getting a specific rating by ID"""
        # Setup
        user = client.post("/users/", json={"username": "user2", "email": "u2@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Movie 2"})
        
        create_response = client.post("/ratings/", json={
            "user_id": user.json()["id"],
            "movie_id": movie.json()["id"],
            "rating": 7.5
        })
        rating_id = create_response.json()["id"]
        
        response = client.get(f"/ratings/{rating_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == rating_id
        assert data["rating"] == 7.5

    def test_get_rating_not_found(self, client):
        """Test getting a non-existent rating"""
        response = client.get("/ratings/999")
        assert response.status_code == 404

    def test_update_rating(self, client):
        """Test updating a rating"""
        # Setup
        user = client.post("/users/", json={"username": "user3", "email": "u3@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Movie 3"})
        
        create_response = client.post("/ratings/", json={
            "user_id": user.json()["id"],
            "movie_id": movie.json()["id"],
            "rating": 6.0
        })
        rating_id = create_response.json()["id"]
        
        update_data = {"rating": 8.5, "review": "Updated review"}
        response = client.put(f"/ratings/{rating_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["rating"] == 8.5
        assert data["review"] == "Updated review"

    def test_delete_rating(self, client):
        """Test deleting a rating"""
        # Setup
        user = client.post("/users/", json={"username": "user4", "email": "u4@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Movie 4"})
        
        create_response = client.post("/ratings/", json={
            "user_id": user.json()["id"],
            "movie_id": movie.json()["id"],
            "rating": 5.0
        })
        rating_id = create_response.json()["id"]
        
        response = client.delete(f"/ratings/{rating_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/ratings/{rating_id}")
        assert get_response.status_code == 404

    def test_get_ratings_by_movie(self, client):
        """Test getting all ratings for a specific movie"""
        # Setup
        user = client.post("/users/", json={"username": "user5", "email": "u5@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Popular Movie"})
        movie_id = movie.json()["id"]
        
        client.post("/ratings/", json={
            "user_id": user.json()["id"],
            "movie_id": movie_id,
            "rating": 9.0
        })
        
        response = client.get(f"/ratings/movie/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_ratings_by_user(self, client):
        """Test getting all ratings by a specific user"""
        # Setup
        user = client.post("/users/", json={"username": "user6", "email": "u6@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "Movie 5"})
        
        client.post("/ratings/", json={
            "user_id": user_id,
            "movie_id": movie.json()["id"],
            "rating": 7.0
        })
        
        response = client.get(f"/ratings/user/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_create_duplicate_rating(self, client):
        """Test that user cannot rate the same movie twice"""
        # Setup
        user = client.post("/users/", json={"username": "user7", "email": "u7@test.com", "password": "pass"})
        movie = client.post("/movies/", json={"title": "Movie 6"})
        
        rating_data = {
            "user_id": user.json()["id"],
            "movie_id": movie.json()["id"],
            "rating": 8.0
        }
        
        # First rating should succeed
        response1 = client.post("/ratings/", json=rating_data)
        assert response1.status_code == 201
        
        # Duplicate rating should fail
        response2 = client.post("/ratings/", json=rating_data)
        assert response2.status_code == 400

    def test_update_rating_not_found(self, client):
        """Test updating non-existent rating"""
        response = client.put("/ratings/999", json={"rating": 5.0})
        assert response.status_code == 404

    def test_delete_rating_not_found(self, client):
        """Test deleting non-existent rating"""
        response = client.delete("/ratings/999")
        assert response.status_code == 404

    def test_create_rating_invalid_user(self, client):
        """Test creating rating with invalid user"""
        movie = client.post("/movies/", json={"title": "Test Movie"})
        movie_id = movie.json()["id"]
        
        rating_data = {
            "user_id": 999,
            "movie_id": movie_id,
            "rating": 5.0
        }
        response = client.post("/ratings/", json=rating_data)
        assert response.status_code == 400

    def test_create_rating_invalid_movie(self, client):
        """Test creating rating with invalid movie"""
        user = client.post("/users/", json={"username": "user8", "email": "u8@test.com", "password": "pass"})
        user_id = user.json()["id"]
        
        rating_data = {
            "user_id": user_id,
            "movie_id": 999,
            "rating": 5.0
        }
        response = client.post("/ratings/", json=rating_data)
        assert response.status_code == 400

    def test_get_all_ratings_empty(self, client):
        """Test getting all ratings when none exist"""
        response = client.get("/ratings/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_ratings_by_nonexistent_movie(self, client):
        """Test getting ratings for non-existent movie"""
        response = client.get("/ratings/movie/999")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_ratings_by_nonexistent_user(self, client):
        """Test getting ratings by non-existent user"""
        response = client.get("/ratings/user/999")
        assert response.status_code == 200
        assert response.json() == []
