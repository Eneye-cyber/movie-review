import pytest
from fastapi import status

class TestUserRegistration:
    def test_register_user_success(self, client):
        """Test successful user registration"""
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123!"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password should not be returned

    def test_register_user_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",  # Already exists
            "email": "newemail@example.com",
            "password": "StrongPass123!"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]

    def test_register_user_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post("/api/auth/register", json={
            "username": "differentuser",
            "email": "test@example.com",  # Already exists
            "password": "StrongPass123!"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]

    def test_register_user_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "weak"  # Too weak
        })
        
        # Update assertion for Pydantic V2 error format
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        # data = response.json()s
       

        # Check if there's any error related to password field
        # assert any("password" in str(error.get("loc", [])) for error in data.get("detail", []))

    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "invalid-email",
            "password": "StrongPass123!"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_invalid_username(self, client):
        """Test registration with invalid username format"""
        response = client.post("/api/auth/register", json={
            "username": "invalid username!",  # Contains invalid characters
            "email": "valid@example.com",
            "password": "StrongPass123!"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestUserLogin:
    def test_login_success(self, client, test_user):
        """Test successful user login"""
        response = client.post("/api/auth/login", data={
            "username": "testuser",
            "password": "testpassword"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post("/api/auth/login", data={
            "username": "testuser",
            "password": "wrongpassword"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post("/api/auth/login", data={
            "username": "nonexistent",
            "password": "somepassword"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_empty_credentials(self, client):
        """Test login with empty credentials"""
        response = client.post("/api/auth/login", data={
            "username": "",
            "password": ""
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

class TestAuthenticationFlow:
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.post("/api/movies/", json={
            "title": "Test Movie",
            "genre": "Drama",
            "release_year": 2020
        })
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/movies/", json={
            "title": "Test Movie",
            "genre": "Drama",
            "release_year": 2020
        }, headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_valid_token(self, client, auth_headers):
        """Test accessing protected endpoint with valid token"""
        response = client.post("/api/movies/", json={
            "title": "Test Movie",
            "genre": "Drama",
            "release_year": 2020,
            "description": "A test movie"
        }, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK