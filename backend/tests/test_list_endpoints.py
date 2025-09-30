import pytest
from fastapi import status

class TestMovieListEndpoint:
    def test_list_movies_empty(self, client):
        """Test listing movies when database is empty"""
        response = client.get("/api/movies/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["movies"] == []
        assert data["page"] == 1
        assert data["limit"] == 10

    def test_list_movies_with_data(self, client, test_movie):
        """Test listing movies with existing data"""
        response = client.get("/api/movies/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["movies"]) == 1
        assert data["movies"][0]["title"] == test_movie.title
        assert data["movies"][0]["genre"] == test_movie.genre

    def test_list_movies_pagination(self, client, auth_headers, db_session):
        """Test movie list pagination"""
        # Create multiple movies
        for i in range(15):
            movie_data = {
                "title": f"Movie {i}",
                "genre": "Drama",
                "release_year": 2000 + i
            }
            client.post("/api/movies/", json=movie_data, headers=auth_headers)
        
        # Test first page
        response = client.get("/api/movies/?page=1&limit=10")
        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 10
        assert data["total"] == 15
        assert len(data["movies"]) == 10
        
        # Test second page
        response = client.get("/api/movies/?page=2&limit=10")
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        assert data["total"] == 15
        assert len(data["movies"]) == 5

    def test_list_movies_filter_by_genre(self, client, auth_headers):
        """Test filtering movies by genre"""
        # Create movies with different genres
        movies = [
            {"title": "Action Movie", "genre": "Action", "release_year": 2020},
            {"title": "Drama Movie", "genre": "Drama", "release_year": 2020},
            {"title": "Another Drama", "genre": "Drama", "release_year": 2021},
        ]
        
        for movie in movies:
            client.post("/api/movies/", json=movie, headers=auth_headers)
        
        # Filter by Drama genre
        response = client.get("/api/movies/?genre=Drama")
        data = response.json()
        
        assert data["total"] == 2
        for movie in data["movies"]:
            assert "Drama" in movie["genre"]

    def test_list_movies_filter_by_year_range(self, client, auth_headers):
        """Test filtering movies by year range"""
        movies = [
            {"title": "Old Movie", "genre": "Drama", "release_year": 1990},
            {"title": "Mid Movie", "genre": "Action", "release_year": 2000},
            {"title": "New Movie", "genre": "Comedy", "release_year": 2010},
        ]
        
        for movie in movies:
            client.post("/api/movies/", json=movie, headers=auth_headers)
        
        # Filter by years 1995-2005
        response = client.get("/api/movies/?min_year=1995&max_year=2005")
        data = response.json()
        
        assert data["total"] == 1
        assert data["movies"][0]["release_year"] == 2000

    def test_list_movies_search(self, client, auth_headers):
        """Test searching movies by title or description"""
        movies = [
            {"title": "The Dark Knight", "genre": "Action", "release_year": 2008, "description": "Batman movie"},
            {"title": "Inception", "genre": "Sci-Fi", "release_year": 2010, "description": "Dream within a dream"},
            {"title": "Interstellar", "genre": "Sci-Fi", "release_year": 2014, "description": "Space adventure"},
        ]
        
        for movie in movies:
            client.post("/api/movies/", json=movie, headers=auth_headers)
        
        # Search for "dream"
        response = client.get("/api/movies/?search=dream")
        data = response.json()
        
        assert data["total"] == 1
        assert "Inception" in data["movies"][0]["title"]

    def test_list_movies_invalid_pagination(self, client):
        """Test list movies with invalid pagination parameters"""
        response = client.get("/api/movies/?page=0&limit=5")  # page should be >= 1
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_movies_combined_filters(self, client, auth_headers):
        """Test combining multiple filters"""
        movies = [
            {"title": "Action 2020", "genre": "Action", "release_year": 2020},
            {"title": "Action 2021", "genre": "Action", "release_year": 2021},
            {"title": "Drama 2020", "genre": "Drama", "release_year": 2020},
            {"title": "Drama 2021", "genre": "Drama", "release_year": 2021},
        ]
        
        for movie in movies:
            client.post("/api/movies/", json=movie, headers=auth_headers)
        
        # Filter Action movies from 2020
        response = client.get("/api/movies/?genre=Action&min_year=2020&max_year=2020")
        data = response.json()
        
        assert data["total"] == 1
        assert data["movies"][0]["title"] == "Action 2020"

class TestRatingListEndpoint:
    def test_list_ratings_for_movie(self, client, test_movie, auth_headers_user2, db_session):
        """Test listing ratings for a specific movie"""
        # Add a rating first
        rating_data = {
            "rating": 4,
            "review": "Good movie"
        }
        
        client.post(
            f"/api/movies/{test_movie.id}/ratings",
            json=rating_data,
            headers=auth_headers_user2
        )
        
        # List ratings for the movie
        response = client.get(f"/api/movies/{test_movie.id}/ratings")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["ratings"]) == 1
        assert data["ratings"][0]["rating"] == 4
        assert data["ratings"][0]["review"] == "Good movie"

    def test_list_ratings_nonexistent_movie(self, client):
        """Test listing ratings for non-existent movie"""
        response = client.get("/api/movies/9999/ratings")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND