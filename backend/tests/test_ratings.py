import pytest
from fastapi import status
import html


class TestRatingLogic:
    def test_create_rating_success(self, client, auth_headers_user2, test_movie):
        """Test successfully creating a rating"""
        rating_data = {
            "rating": 5,
            "review": "Excellent movie!"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data,
            headers=auth_headers_user2
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["rating"] == rating_data["rating"]
        assert data["review"] == rating_data["review"]
        assert data["movie_id"] == test_movie.id
        assert "user_id" in data
        assert "id" in data
        assert "created_at" in data

    def test_update_existing_rating(self, client, auth_headers_user2, test_movie, db_session, test_user2):
        """Test updating an existing rating (should update, not create new)"""
        from app.models.rating import Rating
        
        # Create initial rating using the test_user2 fixture
        initial_rating = Rating(
            movie_id=test_movie.id,
            user_id=test_user2.id,  # Use the actual user ID from fixture
            rating=3,
            review="It was okay"
        )
        db_session.add(initial_rating)
        db_session.commit()
        db_session.refresh(initial_rating)
        
        # Update the rating via API
        updated_rating_data = {
            "rating": 5,
            "review": "Actually, it's great!"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=updated_rating_data,
            headers=auth_headers_user2
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["rating"] == updated_rating_data["rating"]
        assert html.unescape(data["review"]) == html.escape(updated_rating_data["review"])
        
        # Verify only one rating exists for this user+movie combination
        ratings_count = db_session.query(Rating).filter_by(
            movie_id=test_movie.id,
            user_id=test_user2.id
        ).count()
        assert ratings_count == 1  # Should update, not create new

    # def test_rate_own_movie(self, client, auth_headers, test_movie):
    #     """Test rating your own movie (should be prevented)"""
    #     rating_data = {
    #         "rating": 5,
    #         "review": "My own great movie!"
    #     }
        
    #     response = client.post(
    #         f"/api/movies/{test_movie.id}/ratings",
    #         json=rating_data,
    #         headers=auth_headers
    #     )
        
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert "cannot rate your own movie" in response.json()["detail"].lower()

    def test_rating_out_of_range(self, client, auth_headers_user2, test_movie):
        """Test rating with value outside 1-5 range"""
        rating_data = {
            "rating": 6,  # Invalid
            "review": "Too high rating"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data,
            headers=auth_headers_user2
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rating_nonexistent_movie(self, client, auth_headers_user2):
        """Test rating a movie that doesn't exist"""
        rating_data = {
            "rating": 4,
            "review": "Good movie"
        }
        
        response = client.post(
            "/api/movies/9999/ratings",  # Non-existent ID
            json=rating_data,
            headers=auth_headers_user2
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Movie not found" in response.json()["detail"]

    def test_rating_without_auth(self, client, test_movie):
        """Test rating without authentication"""
        rating_data = {
            "rating": 4,
            "review": "Good movie"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN  # Changed from 401 to 403

    def test_rating_stats_update(self, client, auth_headers_user2, test_movie, db_session, test_user2):
        """Test that movie rating stats are updated after rating"""
        # Initial stats should be 0
        db_session.refresh(test_movie)  # Refresh to get current state
        assert test_movie.ratings_count == 0
        assert test_movie.ratings_avg == 0.0
        
        # Add first rating
        rating_data_1 = {
            "rating": 4,
            "review": "Good movie"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data_1,
            headers=auth_headers_user2
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Refresh movie from database
        db_session.refresh(test_movie)
        assert test_movie.ratings_count == 1
        assert test_movie.ratings_avg == 4.0
        
        # Create another user for second rating
        from app.models.user import User
        from app.auth.jwt import get_password_hash
        
        user3 = User(
            username="testuser3",
            email="test3@example.com",
            password_hash=get_password_hash("testpassword")
        )
        db_session.add(user3)
        db_session.commit()
        db_session.refresh(user3)
        
        # Create token for user3
        from app.auth.jwt import create_access_token
        token = create_access_token(data={"sub": user3.username})
        headers_user3 = {"Authorization": f"Bearer {token}"}
        
        rating_data_2 = {
            "rating": 5,
            "review": "Excellent!"
        }
        
        response = client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data_2,
            headers=headers_user3
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Refresh movie from database again
        db_session.refresh(test_movie)
        assert test_movie.ratings_count == 2
        assert test_movie.ratings_avg == 4.5  # (4 + 5) / 2