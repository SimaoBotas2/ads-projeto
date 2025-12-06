# Movie Recommendation API

A FastAPI-based movie recommendation platform with user authentication, movie browsing, and rating functionality.

## Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose

## Features

- User registration and authentication with JWT
- Browse movies with detailed information (genres, directors, cast, ratings)
- Search movies by name
- Filter movies by genre
- Get movie recommendations
- Rate movies (1-5 scale)
- Average rating calculation per movie

## Project Structure

```
ads-projeto/
├── src/
│   ├── api/                    # Backend API
│   │   ├── app/
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   ├── schemas/        # Pydantic schemas
│   │   │   ├── repositories/   # Database operations
│   │   │   ├── services/       # Business logic
│   │   │   ├── routers/        # API endpoints
│   │   │   └── utils/          # Utilities (JWT, etc.)
│   │   ├── alembic/            # Database migrations
│   │   ├── seed_data.py        # Test data seeding script
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── web/                    # Frontend (if applicable)
└── docs/                       # Documentation
```

## Getting Started

### Prerequisites

- Docker Desktop installed and running
- Git (to clone the repository)

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://gitlab.com/botassimao/ads-projeto.git
   cd ads-projeto
   ```

2. **Navigate to the API directory**

   ```bash
   cd src/api
   ```

3. **Build and start the containers**

   ```bash
   docker compose up --build
   ```

   This will:

   - Build the FastAPI application image
   - Start PostgreSQL database container
   - Start the API container
   - Run database migrations automatically
   - Start the API server on http://localhost:5000

4. **Seed the database with test data** (in a new terminal)

   ```bash
   docker compose exec api python seed_data.py
   ```

### Accessing the API

- **API Documentation (Swagger UI)**: http://localhost:5000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## API Endpoints

### Authentication

- `POST /users/register` - Register a new user
- `POST /users/login` - Login and receive JWT token

### Movies

- `GET /movies/` - List all movies
- `GET /movies/{movie_id}` - Get movie details with average rating
- `GET /movies/search/?query={query}` - Search movies by name
- `GET /movies/genre/{genre_id}` - Get movies by genre
- `GET /movies/recommendations/top` - Get top recommended movies

### Users

- `GET /users/{user_id}` - Get user profile
- `PUT /users/{user_id}` - Update user profile
- `DELETE /users/{user_id}` - Delete user

### Ratings

- `POST /ratings/` - Create a new rating
- `GET /ratings/user/{user_id}` - Get all ratings by a user
- `GET /ratings/movie/{movie_id}` - Get all ratings for a movie

### Genres, Directors, Cast

- `GET /genres/` - List all genres
- `GET /directors/` - List all directors
- `GET /cast/` - List all cast members

## Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:5000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "name": "New User",
    "password": "securepassword"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "password123"
  }'
```

### Get movie details

```bash
curl http://localhost:5000/movies/1
```

### Search movies

```bash
curl http://localhost:5000/movies/search/?query=inception
```

## Development

### Stop the containers

```bash
docker compose down
```

### Restart after code changes

```bash
docker compose restart api
```

### Rebuild after dependency changes

```bash
docker compose down
docker compose up --build
```

### View logs

```bash
docker compose logs api --tail 50
```

### Access the database directly

```bash
docker compose exec db psql -U postgres -d movie_recommendation
```

## Database Schema

The application uses the following main tables:

- `movie` - Movie information
- `genre` - Movie genres
- `director` - Movie directors
- `cast` - Cast members
- `_user_` - User accounts
- `rating` - Movie ratings by users
- Association tables for many-to-many relationships

## Environment Variables

Default configuration in `docker-compose.yml`:

- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

## Testing

Test the API endpoints using:

- Swagger UI at http://localhost:5000/docs (interactive testing)
- Postman or any HTTP client
- curl commands (see examples above)

## Notes

- All passwords are hashed using SHA-256 with salt
- JWT tokens expire after 30 minutes
- The `last_login` field updates automatically on user login
- Movie ratings are on a scale of 1-5
- Average ratings are calculated dynamically when fetching movie details

## Troubleshooting

**Containers won't start**: Ensure Docker Desktop is running and ports 5000 and 5432 are not in use.

**Database connection errors**: Wait a few seconds for PostgreSQL to fully initialize on first startup.

**Changes not reflected**: Restart the API container with `docker compose restart api`.

**Need to reset database**: Run `docker compose down -v` to remove volumes, then `docker compose up --build`.

## License

This project is part of an academic assignment for the ADS course.
