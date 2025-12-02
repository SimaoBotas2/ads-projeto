"""Integration tests for Ratings Router with correct API parameters"""


class TestRatingsRouter:
    """Integration tests for Ratings Router"""

    def test_create_rating_correct_api(self, client):
        """Test creating a new rating with correct API parameters"""
        # Create user and movie first
        user_response = client.post("/users/", json={
            "username": "rater",
            "email": "rater@test.com",
            "password": "pass123"
        })
        user_id = user_response.json()["id"]
        
        movie_response = client.post("/movies/", json={"title": "Interstellar"})
        movie_id = movie_response.json()["id"]
        
        # Create rating with evaluation (1-4 range)
        rating_data = {"movie_id": movie_id, "evaluation": 4}
        response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        assert response.status_code == 201
        data = response.json()
        assert data["evaluation"] == 4
        assert "id" in data

    def test_get_user_ratings(self, client):
        """Test getting all ratings by a specific user"""
        # Setup user and movie
        user = client.post("/users/", json={"username": "rater1", "email": "r1@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "TestMovie1"})
        movie_id = movie.json()["id"]
        
        # Create rating
        rating_data = {"movie_id": movie_id, "evaluation": 3}
        client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        
        # Get user ratings
        response = client.get(f"/ratings/user/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["evaluation"] == 3

    def test_get_movie_ratings(self, client):
        """Test getting all ratings for a specific movie"""
        # Setup
        user = client.post("/users/", json={"username": "rater2", "email": "r2@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "PopularMovie"})
        movie_id = movie.json()["id"]
        
        # Create rating
        rating_data = {"movie_id": movie_id, "evaluation": 2}
        client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        
        # Get movie ratings
        response = client.get(f"/ratings/movie/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["evaluation"] == 2

    def test_update_rating(self, client):
        """Test updating a rating"""
        # Setup
        user = client.post("/users/", json={"username": "rater3", "email": "r3@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "UpdateMovie"})
        movie_id = movie.json()["id"]
        
        # Create rating
        rating_data = {"movie_id": movie_id, "evaluation": 1}
        create_response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        rating_id = create_response.json()["id"]
        
        # Update rating
        update_data = {"evaluation": 4}
        response = client.put(f"/ratings/{rating_id}?user_id={user_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["evaluation"] == 4

    def test_delete_rating(self, client):
        """Test deleting a rating"""
        # Setup
        user = client.post("/users/", json={"username": "rater4", "email": "r4@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "DeleteMovie"})
        movie_id = movie.json()["id"]
        
        # Create rating
        rating_data = {"movie_id": movie_id, "evaluation": 3}
        create_response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        rating_id = create_response.json()["id"]
        
        # Delete rating
        response = client.delete(f"/ratings/{rating_id}?user_id={user_id}")
        assert response.status_code == 204
        
        # Verify deletion (expect empty list when getting by user)
        get_response = client.get(f"/ratings/user/{user_id}")
        assert len(get_response.json()) == 0

    def test_update_rating_not_found(self, client):
        """Test updating non-existent rating"""
        user = client.post("/users/", json={"username": "user", "email": "u@test.com", "password": "pass"})
        user_id = user.json()["id"]
        response = client.put(f"/ratings/999?user_id={user_id}", json={"evaluation": 2})
        assert response.status_code == 404

    def test_delete_rating_not_found(self, client):
        """Test deleting non-existent rating"""
        user = client.post("/users/", json={"username": "user2", "email": "u2@test.com", "password": "pass"})
        user_id = user.json()["id"]
        response = client.delete(f"/ratings/999?user_id={user_id}")
        assert response.status_code == 404

    def test_get_user_ratings_empty(self, client):
        """Test getting ratings for user with no ratings"""
        user = client.post("/users/", json={"username": "emptyrater", "email": "empty@test.com", "password": "pass"})
        user_id = user.json()["id"]
        response = client.get(f"/ratings/user/{user_id}")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_movie_ratings_empty(self, client):
        """Test getting ratings for movie with no ratings"""
        movie = client.post("/movies/", json={"title": "UnratedMovie"})
        movie_id = movie.json()["id"]
        response = client.get(f"/ratings/movie/{movie_id}")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_rating_invalid_evaluation(self, client):
        """Test creating rating with invalid evaluation value"""
        user = client.post("/users/", json={"username": "badrating", "email": "bad@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "BadMovie"})
        movie_id = movie.json()["id"]
        
        # Try with evaluation outside range (should fail due to CheckConstraint)
        rating_data = {"movie_id": movie_id, "evaluation": 5}
        response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        assert response.status_code in [400, 422]

    def test_create_rating_missing_evaluation(self, client):
        """Test creating rating without evaluation field"""
        user = client.post("/users/", json={"username": "noeval", "email": "noeval@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "NoEvalMovie"})
        movie_id = movie.json()["id"]
        
        # Try without evaluation (should fail validation)
        rating_data = {"movie_id": movie_id}
        response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        assert response.status_code == 422

    def test_multiple_ratings_same_movie(self, client):
        """Test multiple users can rate the same movie"""
        movie = client.post("/movies/", json={"title": "SharedMovie"})
        movie_id = movie.json()["id"]
        
        # Multiple users rate same movie
        for i in range(3):
            user = client.post("/users/", json={
                "username": f"rater{i}",
                "email": f"rater{i}@test.com",
                "password": "pass"
            })
            user_id = user.json()["id"]
            rating_data = {"movie_id": movie_id, "evaluation": i + 1}
            response = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
            assert response.status_code == 201
        
        # Get all ratings for movie
        response = client.get(f"/ratings/movie/{movie_id}")
        assert len(response.json()) == 3

    def test_user_cannot_rate_same_movie_twice(self, client):
        """Test that user cannot rate the same movie twice"""
        user = client.post("/users/", json={"username": "dupuser", "email": "dup@test.com", "password": "pass"})
        user_id = user.json()["id"]
        movie = client.post("/movies/", json={"title": "DupMovie"})
        movie_id = movie.json()["id"]
        
        # First rating
        rating_data = {"movie_id": movie_id, "evaluation": 2}
        response1 = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        assert response1.status_code == 201
        
        # Duplicate rating should fail
        response2 = client.post(f"/ratings/?user_id={user_id}", json=rating_data)
        assert response2.status_code == 400

    def test_evaluation_range_boundaries(self, client):
        """Test evaluation values at boundary (1 and 4)"""
        user = client.post("/users/", json={"username": "boundary", "email": "boundary@test.com", "password": "pass"})
        user_id = user.json()["id"]
        
        # Test with evaluation 1 (min)
        movie1 = client.post("/movies/", json={"title": "MinMovie"})
        movie1_id = movie1.json()["id"]
        response1 = client.post(f"/ratings/?user_id={user_id}", json={"movie_id": movie1_id, "evaluation": 1})
        assert response1.status_code == 201
        assert response1.json()["evaluation"] == 1
        
        # Test with evaluation 4 (max)
        movie2 = client.post("/movies/", json={"title": "MaxMovie"})
        movie2_id = movie2.json()["id"]
        response2 = client.post(f"/ratings/?user_id={user_id}", json={"movie_id": movie2_id, "evaluation": 4})
        assert response2.status_code == 201
        assert response2.json()["evaluation"] == 4
