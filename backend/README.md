# Movie Rating Platform

A movie rating platform built with FastAPI, SQLAlchemy, and SQLite. Users can register, add movies, and rate/review movies with proper authentication and authorization.

## Features

- **User Authentication**: JWT-based registration and login
- **Movie Management**: Add, view, search, and delete movies
- **Rating System**: Rate movies (1-5 stars) with optional reviews
- **Advanced Filtering**: Search by genre, year range, keywords
- **Pagination**: Efficient data loading for large datasets
- **Input Validation & Sanitization**: Protection against XSS and injection attacks
- **Comprehensive Testing**: Unit tests for all core functionality
- **Database Seeding**: Sample data for development and demonstration

## Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with password hashing
- **Validation**: Pydantic with custom validators
- **Testing**: Pytest with test database
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Quick Start

### Prerequisites

- Python > 3.8  
- pip (Python package manager)

### Installation & Setup

1. **Clone and setup the project**:
```bash
# Create virtual environment (avoid using python > 3.12)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Initialize database**:
```bash
# Apply migration
alembic upgrade head
```

4. **Run the application**:
```bash
fastapi dev app\main.py
```

The application will be available at `http://localhost:8000`

## API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Movies
- `POST /api/movies` - Add new movie (protected)
- `GET /api/movies` - List movies with filtering/pagination
- `GET /api/movies/{id}` - Get movie details
- `DELETE /api/movies/{id}` - Delete movie (creator only)

### Ratings
- `POST /api/movies/{id}/ratings` - Add/update rating (protected)
- `GET /api/movies/{id}/ratings` - List ratings for a movie
- `GET /api/users/{id}/ratings` - List ratings by a user

## Testing

### Running Tests

```bash
# Run all tests
pytest


# Run specific test file
pytest tests/test_auth.py

```

### Test Coverage

The test suite covers:
- User registration and authentication flows
- Movie creation and management
- Rating logic (create vs update)
- List endpoints with filtering and pagination
- Input validation and error handling
- Authentication and authorization

## Database Seeding

### Populate with Sample Data

```bash
# Basic seeding (20 users, 50 movies, 5 ratings per movie)
python seed_database.py

# Custom seeding
python seed_database.py --users 30 --movies 100 --ratings-per-movie 8

# Minimal seeding for testing
python seed_database.py --users 5 --movies 10 --ratings-per-movie 2
```

### Sample Test Accounts

After seeding, use these test accounts:
- **Username**: `admin`, **Password**: `Admin123!`
- **Username**: `john_doe`, **Password**: `Password123!`
- **Username**: `jane_smith`, **Password**: `Password123!`

## Project Structure

```
movie_rating_platform/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── crud/            # Database operations
│   ├── api/endpoints/   # Route handlers
│   ├── auth/            # Authentication utilities
│   ├── seeders/         # Database seeding
│   └── database.py      # Database configuration
├── tests/               # Test suite
├── requirements.txt     # Dependencies
└── seed_database.py    # Seeder script
```

## Design Decisions & Architecture

### Modular Design Pattern

The application follows a clean modular architecture:

1. **Models** (`app/models/`): SQLAlchemy ORM models representing database tables
2. **Schemas** (`app/schemas/`): Pydantic models for request/response validation
3. **CRUD Operations** (`app/crud/`): Database interaction layer separating business logic from data access
4. **API Endpoints** (`app/api/endpoints/`): Route handlers using dependency injection
5. **Authentication** (`app/auth/`): JWT token handling and security utilities

### Security Implementation

#### Input Validation & Sanitization
- **Pydantic Validators**: All inputs are validated using Pydantic with custom validators
- **HTML Escaping**: Potential XSS vectors are neutralized using `html.escape()` before storage
- **SQL Injection Protection**: SQLAlchemy ORM prevents injection, all queries are parameterized

```python
@field_validator('title', 'genre', 'description')
def sanitize_text(cls, v):
    """Basic HTML sanitization to prevent XSS"""
    if v is None:
        return v
    return html.escape(v)
```

#### Authentication & Authorization
- **JWT Tokens**: Stateless authentication using JSON Web Tokens
- **Password Hashing**: BCrypt for secure password storage
- **Protected Endpoints**: Route protection using FastAPI dependencies
- **Ownership Verification**: Users can only delete their own movies

### Performance Optimizations

#### Aggregated Rating Fields
Movies store `ratings_count` and `ratings_avg` to avoid expensive JOIN operations:

```python
# In Movie model
ratings_count = Column(Integer, default=0)
ratings_avg = Column(Float, default=0.0)
```

These fields are updated automatically when ratings are added/updated, enabling fast queries for movie listings without calculating aggregates on-the-fly.

#### Efficient Filtering & Pagination
List endpoints support multiple filter parameters and pagination to handle large datasets efficiently:

```python
# Supports: genre, year range, search, pagination
GET /api/movies/?genre=Action&min_year=2000&max_year=2020&search=batman&page=1&limit=10
```

### Business Logic Enforcement

#### Unique Ratings Constraint
The database enforces one rating per user per movie using a unique constraint:

```python
# In Rating model
__table_args__ = (UniqueConstraint('movie_id', 'user_id', name='unique_user_movie_rating'),)
```

The application handles this by updating existing ratings rather than creating duplicates.

#### Self-Rating Prevention
Users cannot rate their own movies, enforced at the API layer: (Optional, currently disabled as it wasn't requested)

```python
if movie.created_by == current_user.id:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You cannot rate your own movie"
    )
```

### Error Handling

Comprehensive error handling with appropriate HTTP status codes:
- `400 Bad Request`: Validation errors, business rule violations
- `401 Unauthorized`: Invalid or missing authentication
- `403 Forbidden`: Authenticated but not authorized for action
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Input validation failures

### Testing Strategy

- **Test Database**: In-memory SQLite database for isolated testing
- **Fixture-Based**: Reusable test fixtures for users, movies, authentication
- **Coverage**: Tests for success paths, error conditions, and edge cases
- **Integration Tests**: End-to-end testing of API workflows

## Development

### Adding New Features

1. **Add Model**: Define SQLAlchemy model in `app/models/`
2. **Create Schema**: Define Pydantic schemas in `app/schemas/`
3. **Implement CRUD**: Add database operations in `app/crud/`
4. **Create Endpoints**: Add route handlers in `app/api/endpoints/`
5. **Write Tests**: Add comprehensive tests in `tests/`

### Database Migrations

While the project uses SQLAlchemy's `create_all()` for simplicity, for production you might want to use Alembic:

```bash
# Initialize alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Production Considerations

1. **CORS**: Configure proper CORS settings for your frontend
2. **Rate Limiting**: Implement rate limiting on authentication endpoints
3. **Logging**: Add structured logging for monitoring
4. **HTTPS**: Always use HTTPS in production

## License

This project is licensed under the MIT License.