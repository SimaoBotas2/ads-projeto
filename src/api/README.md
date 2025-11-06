# Movie Recommendation Platform API

A FastAPI-based backend for a movie recommendation platform.

## Project Structure

```
src/api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   ├── cast.py
│   │   └── rating.py
│   ├── schemas/             # Pydantic schemas for validation
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   ├── cast.py
│   │   └── rating.py
│   ├── repositories/        # Data access layer
│   │   ├── user_repository.py
│   │   ├── movie_repository.py
│   │   ├── genre_repository.py
│   │   ├── director_repository.py
│   │   ├── cast_repository.py
│   │   └── rating_repository.py
│   ├── services/            # Business logic layer
│   │   ├── user_service.py
│   │   ├── movie_service.py
│   │   └── rating_service.py
│   ├── controllers/         # Request handlers
│   │   └── controllers.py
│   └── routers/             # API route definitions
│       ├── users.py
│       ├── movies.py
│       ├── genres.py
│       ├── directors.py
│       ├── cast.py
│       └── ratings.py
├── alembic/                 # Database migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Database Schema

### Entities

- **User**: User accounts with authentication
- **Movie**: Movie information and metadata
- **Genre**: Movie genres
- **Director**: Movie directors
- **Cast**: Cast members/actors
- **Rating**: User ratings and reviews for movies

### Relationships

- User → Rating (one-to-many)
- Movie → Rating (one-to-many)
- Movie ↔ Genre (many-to-many)
- Movie ↔ Director (many-to-many)
- Movie ↔ Cast (many-to-many)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

### Setup

1. **Copy environment variables**

   ```bash
   cp .env.example .env
   ```

2. **Start PostgreSQL database**

   ```bash
   docker-compose up postgres -d
   ```

3. **Install dependencies** (for local development)

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database migrations**

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

5. **Run the application**

   Using Docker:

   ```bash
   docker-compose up
   ```

   Or locally:

   ```bash
   uvicorn app.main:app --reload --port 5000
   ```

6. **Access the API**
   - API: http://localhost:5000
   - Swagger Docs: http://localhost:5000/docs
   - ReDoc: http://localhost:5000/redoc

## Development Guide

### Adding New Features

1. **Create/Update Models** in `app/models/`
2. **Create/Update Schemas** in `app/schemas/`
3. **Create/Update Repositories** in `app/repositories/`
4. **Create/Update Services** in `app/services/`
5. **Create/Update Routers** in `app/routers/`
6. **Generate Migration**: `alembic revision --autogenerate -m "description"`
7. **Apply Migration**: `alembic upgrade head`

### Database Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## API Endpoints (TODO)

### Users

- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Movies

- `GET /movies/` - List all movies
- `POST /movies/` - Create movie
- `GET /movies/search` - Search movies
- `GET /movies/{movie_id}` - Get movie details
- `PUT /movies/{movie_id}` - Update movie
- `DELETE /movies/{movie_id}` - Delete movie
- `GET /movies/recommendations/{user_id}` - Get recommendations

### Genres

- `GET /genres/` - List all genres
- `POST /genres/` - Create genre
- `GET /genres/{genre_id}` - Get genre details
- `PUT /genres/{genre_id}` - Update genre
- `DELETE /genres/{genre_id}` - Delete genre

### Directors

- `GET /directors/` - List all directors
- `POST /directors/` - Create director
- `GET /directors/{director_id}` - Get director details
- `PUT /directors/{director_id}` - Update director
- `DELETE /directors/{director_id}` - Delete director

### Cast

- `GET /cast/` - List all cast members
- `POST /cast/` - Create cast member
- `GET /cast/{cast_id}` - Get cast details
- `PUT /cast/{cast_id}` - Update cast member
- `DELETE /cast/{cast_id}` - Delete cast member

### Ratings

- `POST /ratings/` - Create/Update rating
- `GET /ratings/user/{user_id}` - Get user's ratings
- `GET /ratings/movie/{movie_id}` - Get movie's ratings
- `PUT /ratings/{rating_id}` - Update rating
- `DELETE /ratings/{rating_id}` - Delete rating

## Next Steps

1. Implement repository methods for database operations
2. Implement service layer business logic
3. Implement authentication (JWT tokens)
4. Implement API endpoints in routers
5. Add recommendation algorithm
6. Add input validation and error handling
7. Add unit and integration tests
8. Add API documentation
9. Implement caching (Redis)
10. Add logging and monitoring
