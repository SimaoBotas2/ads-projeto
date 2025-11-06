# Movie Recommendation Platform - Project Overview

## 🎯 Project Goal

A simple movie recommendation platform designed to help users discover new titles that match their interests.

## 📊 Database Entities & Relationships

```
┌──────────┐       ┌──────────┐       ┌──────────┐
│  User    │       │  Rating  │       │  Movie   │
├──────────┤       ├──────────┤       ├──────────┤
│ id (PK)  │───┐   │ id (PK)  │   ┌───│ id (PK)  │
│ username │   └──→│ user_id  │   │   │ title    │
│ email    │       │ movie_id │←──┘   │ overview │
│ password │       │ rating   │       │ ...      │
│ ...      │       │ review   │       └──────────┘
└──────────┘       └──────────┘            │
                                           │ M:N
                                           │
                   ┌───────────────────────┼───────────────┐
                   │                       │               │
              ┌────▼────┐          ┌──────▼───┐    ┌──────▼─────┐
              │  Genre  │          │ Director │    │    Cast    │
              ├─────────┤          ├──────────┤    ├────────────┤
              │ id (PK) │          │ id (PK)  │    │ id (PK)    │
              │ name    │          │ name     │    │ name       │
              └─────────┘          │ bio      │    │ bio        │
                                   └──────────┘    └────────────┘
```

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Users   │  │  Movies  │  │ Ratings  │  ...        │
│  │  Router  │  │  Router  │  │  Router  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────────────────┐
│                 Controller Layer                        │
│        (Handles HTTP requests/responses)                │
└───────┬─────────────┬─────────────┬────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────────────────┐
│                  Service Layer                          │
│         (Business logic & validation)                   │
└───────┬─────────────┬─────────────┬────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────────────────┐
│                Repository Layer                         │
│           (Database operations - CRUD)                  │
└───────┬─────────────┬─────────────┬────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────────────────┐
│                 Database Layer                          │
│         PostgreSQL with SQLAlchemy ORM                  │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
src/api/
├── app/
│   ├── config.py              # App configuration & settings
│   ├── database.py            # DB connection & session management
│   ├── main.py                # FastAPI app initialization
│   │
│   ├── models/                # SQLAlchemy ORM Models (Database Tables)
│   │   ├── user.py           # ✅ Implemented
│   │   ├── movie.py          # ✅ Implemented
│   │   ├── genre.py          # ✅ Implemented
│   │   ├── director.py       # ✅ Implemented
│   │   ├── cast.py           # ✅ Implemented
│   │   └── rating.py         # ✅ Implemented
│   │
│   ├── schemas/               # Pydantic Schemas (Validation & Serialization)
│   │   ├── user.py           # ✅ Implemented
│   │   ├── movie.py          # ✅ Implemented
│   │   ├── genre.py          # ✅ Implemented
│   │   ├── director.py       # ✅ Implemented
│   │   ├── cast.py           # ✅ Implemented
│   │   └── rating.py         # ✅ Implemented
│   │
│   ├── repositories/          # Data Access Layer
│   │   ├── user_repository.py        # 🔲 TODO: Implement
│   │   ├── movie_repository.py       # 🔲 TODO: Implement
│   │   ├── genre_repository.py       # 🔲 TODO: Implement
│   │   ├── director_repository.py    # 🔲 TODO: Implement
│   │   ├── cast_repository.py        # 🔲 TODO: Implement
│   │   └── rating_repository.py      # 🔲 TODO: Implement
│   │
│   ├── services/              # Business Logic Layer
│   │   ├── user_service.py           # 🔲 TODO: Implement
│   │   ├── movie_service.py          # 🔲 TODO: Implement
│   │   └── rating_service.py         # 🔲 TODO: Implement
│   │
│   ├── controllers/           # Request Handlers
│   │   └── controllers.py            # 🔲 TODO: Implement
│   │
│   └── routers/               # API Endpoints
│       ├── users.py                  # 🔲 TODO: Implement routes
│       ├── movies.py                 # 🔲 TODO: Implement routes
│       ├── genres.py                 # 🔲 TODO: Implement routes
│       ├── directors.py              # 🔲 TODO: Implement routes
│       ├── cast.py                   # 🔲 TODO: Implement routes
│       └── ratings.py                # 🔲 TODO: Implement routes
│
├── alembic/                   # Database Migrations
│   ├── versions/             # Migration files
│   └── env.py               # ✅ Configured
│
├── docker-compose.yml        # ✅ PostgreSQL + API setup
├── Dockerfile                # ✅ API container
├── requirements.txt          # ✅ Python dependencies
├── alembic.ini              # ✅ Alembic configuration
├── .env.example             # ✅ Environment variables template
├── setup.ps1                # ✅ Windows setup script
├── setup.sh                 # ✅ Linux/Mac setup script
└── README.md                # ✅ Documentation
```

## 🚀 Quick Start

### Option 1: Using Setup Scripts (Recommended)

**Windows (PowerShell):**

```powershell
cd src/api
.\setup.ps1
```

**Linux/Mac:**

```bash
cd src/api
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Create environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start PostgreSQL:**

   ```bash
   docker-compose up postgres -d
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

5. **Start the API:**
   ```bash
   uvicorn app.main:app --reload --port 5000
   ```

### Option 3: Full Docker Setup

```bash
docker-compose up
```

## 📝 Implementation Checklist

### ✅ Completed

- [x] Project structure setup
- [x] Database models (User, Movie, Genre, Director, Cast, Rating)
- [x] Pydantic schemas for all entities
- [x] Database configuration with PostgreSQL
- [x] Docker & Docker Compose setup
- [x] Alembic migration configuration
- [x] Repository layer structure
- [x] Service layer structure
- [x] Router structure
- [x] Main FastAPI app setup
- [x] CORS middleware configuration
- [x] Documentation

### 🔲 TODO (Your Implementation Tasks)

#### 1. Repository Layer (Database Operations)

- [ ] Implement `UserRepository` methods (CRUD operations)
- [ ] Implement `MovieRepository` methods
- [ ] Implement `GenreRepository` methods
- [ ] Implement `DirectorRepository` methods
- [ ] Implement `CastRepository` methods
- [ ] Implement `RatingRepository` methods

#### 2. Service Layer (Business Logic)

- [ ] Implement `UserService` (authentication, password hashing)
- [ ] Implement `MovieService` (search, filtering)
- [ ] Implement `RatingService` (rating logic, averages)
- [ ] Implement recommendation algorithm

#### 3. API Endpoints (Routes)

- [ ] Users: register, login, CRUD operations
- [ ] Movies: CRUD, search, filter by genre
- [ ] Genres: CRUD operations
- [ ] Directors: CRUD operations
- [ ] Cast: CRUD operations
- [ ] Ratings: CRUD, get by user/movie

#### 4. Additional Features

- [ ] JWT authentication
- [ ] Password hashing (bcrypt)
- [ ] Input validation & error handling
- [ ] Pagination for list endpoints
- [ ] Search functionality
- [ ] Movie recommendation algorithm
- [ ] Unit tests
- [ ] Integration tests
- [ ] API rate limiting
- [ ] Caching (Redis)
- [ ] Logging

## 🎓 Development Tips

### Creating a Repository Method Example

```python
def get_by_id(self, user_id: int) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()
```

### Creating a Service Method Example

```python
def get_user(self, user_id: int) -> Optional[UserResponse]:
    user = self.repository.get_by_id(user_id)
    if user:
        return UserResponse.from_orm(user)
    return None
```

### Creating a Route Example

```python
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## 📚 Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **Alembic** - Database migrations
- **Docker** - Containerization
- **Uvicorn** - ASGI server

## 🌐 API Documentation

Once running, visit:

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## 🎯 Next Steps

1. Start with implementing the Repository layer for one entity (e.g., User)
2. Implement the corresponding Service layer
3. Create API endpoints in the Router
4. Test with the Swagger UI
5. Repeat for other entities
6. Add authentication
7. Implement recommendation algorithm
8. Add tests

Good luck with your implementation! 🚀
