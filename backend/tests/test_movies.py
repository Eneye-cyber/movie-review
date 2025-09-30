import pytest
from fastapi import status

class TestMovieCreation:
    def test_create_movie_success(self, client, auth_headers):
        """Test successful movie creation"""
        movie_data = {
            "title": "The Shawshank Redemption",
            "genre": "Drama",
            "release_year": 1994,
            "description": "Two imprisoned men bond over a number of years."
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == movie_data["title"]
        assert data["genre"] == movie_data["genre"]
        assert data["release_year"] == movie_data["release_year"]
        assert data["description"] == movie_data["description"]
        assert data["ratings_count"] == 0
        assert data["ratings_avg"] == 0.0
        assert "id" in data
        assert "created_by" in data
        assert "created_at" in data

    def test_create_movie_without_auth(self, client):
        """Test movie creation without authentication"""
        movie_data = {
            "title": "Test Movie",
            "genre": "Drama",
            "release_year": 2020
        }
        
        response = client.post("/api/movies/", json=movie_data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_movie_invalid_data(self, client, auth_headers):
        """Test movie creation with invalid data"""
        # Missing required fields
        movie_data = {
            "genre": "Drama",
            "release_year": 2020
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_movie_invalid_year(self, client, auth_headers):
        """Test movie creation with invalid release year"""
        movie_data = {
            "title": "Future Movie",
            "genre": "Sci-Fi",
            "release_year": 3000  # Too far in the future
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_movie_invalid_genre(self, client, auth_headers):
        """Test movie creation with invalid genre"""
        movie_data = {
            "title": "Test Movie",
            "genre": "Invalid@Genre!",  # Invalid characters
            "release_year": 2020
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_movie_empty_title(self, client, auth_headers):
        """Test movie creation with empty title"""
        movie_data = {
            "title": "   ",  # Only whitespace
            "genre": "Drama",
            "release_year": 2020
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_movie_xss_attempt(self, client, auth_headers):
        """Test movie creation with potential XSS payload"""
        movie_data = {
            "title": "<script>alert('xss')</script>",
            "genre": "Drama",
            "release_year": 2020,
            "description": "<img src=x onerror=alert(1)>"
        }
        
        response = client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # The HTML should be escaped
        assert "<script>" not in data["title"]
        assert "<img" not in data["description"]