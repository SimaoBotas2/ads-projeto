# Quick Reference - Movie Recommendation Platform

## 🏗️ Complete Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT                                  │
│                    (Web Browser / Mobile)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ROUTERS (app/routers/)                                    │ │
│  │  /users  /movies  /genres  /directors  /cast  /ratings    │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  SERVICES (app/services/)                                  │ │
│  │  Business Logic, Validation, Authentication                │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  REPOSITORIES (app/repositories/)                          │ │
│  │  Database Operations (CRUD)                                │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
└────────────────────────────┼─────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE                             │
│  Tables: users, movies, genres, directors, cast, ratings        │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Database Tables & Relationships

### Core Tables

```
┌──────────────┐
│    users     │
├──────────────┤
│ id (PK)      │─────┐
│ username     │     │
│ email        │     │
│ password     │     │
└──────────────┘     │
                     │
                     │ 1:N
                     ▼
              ┌──────────────┐
              │   ratings    │
              ├──────────────┤
              │ id (PK)      │
              │ user_id (FK) │
              │ movie_id (FK)│◄─────┐
              │ rating       │      │
              │ review       │      │ 1:N
              └──────────────┘      │
                                   │
                            ┌──────────────┐
                            │   movies     │
                            ├──────────────┤
                            │ id (PK)      │
                            │ title        │
                            │ overview     │
                            │ release_date │
                            └──────┬───────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │ M:N              │ M:N              │ M:N
                ▼                  ▼                  ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │   genres     │  │  directors   │  │     cast     │
        ├──────────────┤  ├──────────────┤  ├──────────────┤
        │ id (PK)      │  │ id (PK)      │  │ id (PK)      │
        │ name         │  │ name         │  │ name         │
        └──────────────┘  │ biography    │  │ biography    │
                          └──────────────┘  └──────────────┘
```

### Junction Tables (for M:N relationships)

- `movie_genre`: movie_id, genre_id
- `movie_director`: movie_id, director_id
- `movie_cast`: movie_id, cast_id, character_name

## 🔄 Request Flow Example

### Example: User creates a rating

```
1. POST /ratings/
   {
     "movie_id": 1,
     "rating": 8.5,
     "review": "Great movie!"
   }
   │
   ▼
2. RatingRouter
   ├─ Validate request body (Pydantic)
   ├─ Get DB session
   └─ Call RatingService
      │
      ▼
3. RatingService
   ├─ Check if user already rated this movie
   ├─ Validate rating value
   └─ Call RatingRepository
      │
      ▼
4. RatingRepository
   ├─ Create Rating object
   ├─ Insert into database
   └─ Return created rating
      │
      ▼
5. RatingService
   └─ Convert to RatingResponse schema
      │
      ▼
6. RatingRouter
   └─ Return JSON response (201 Created)
```

## 📝 File Responsibilities

### Models (app/models/)

**Purpose**: Define database table structure
**Example**:

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    # ...
```

### Schemas (app/schemas/)

**Purpose**: Validate input/output data
**Example**:

```python
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
```

### Repositories (app/repositories/)

**Purpose**: Database CRUD operations
**Example**:

```python
def get_by_id(self, user_id: int):
    return self.db.query(User).filter(User.id == user_id).first()
```

### Services (app/services/)

**Purpose**: Business logic
**Example**:

```python
def create_user(self, user: UserCreate):
    # Hash password
    # Check uniqueness
    # Call repository
```

### Routers (app/routers/)

**Purpose**: API endpoint definitions
**Example**:

```python
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)
```

## 🎯 Implementation Priority

### Priority 1: Essential (Implement First)

1. ✅ Genre CRUD
2. ✅ User registration & login
3. ✅ Movie CRUD
4. ✅ Rating CRUD

### Priority 2: Important

5. ⭐ Search functionality
6. ⭐ Filter by genre
7. ⭐ User profile management
8. ⭐ Movie details with all relationships

### Priority 3: Advanced

9. 🚀 Recommendation algorithm
10. 🚀 JWT authentication
11. 🚀 Caching
12. 🚀 Advanced search filters

## 🛠️ Development Commands Cheatsheet

```powershell
# Setup
cd src/api
.\setup.ps1

# Start database only
docker-compose up postgres -d

# Start everything
docker-compose up

# Stop everything
docker-compose down

# Install dependencies
pip install -r requirements.txt

# Database migrations
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1

# Run API
uvicorn app.main:app --reload --port 5000

# Access PostgreSQL
docker exec -it movie_recommendation_db psql -U user -d movie_recommendation_db
```

## 📍 Key Endpoints Structure

```
/users
  POST   /register         - Create account
  POST   /login            - Login
  GET    /{user_id}        - Get user info
  PUT    /{user_id}        - Update user
  DELETE /{user_id}        - Delete user

/movies
  GET    /                 - List all movies
  POST   /                 - Create movie
  GET    /search?q=query   - Search movies
  GET    /{movie_id}       - Get movie details
  PUT    /{movie_id}       - Update movie
  DELETE /{movie_id}       - Delete movie
  GET    /recommendations/{user_id} - Get recommendations

/genres
  GET    /                 - List all genres
  POST   /                 - Create genre
  GET    /{genre_id}       - Get genre
  PUT    /{genre_id}       - Update genre
  DELETE /{genre_id}       - Delete genre

/directors
  GET    /                 - List all directors
  POST   /                 - Create director
  GET    /{director_id}    - Get director
  PUT    /{director_id}    - Update director
  DELETE /{director_id}    - Delete director

/cast
  GET    /                 - List all cast
  POST   /                 - Create cast member
  GET    /{cast_id}        - Get cast member
  PUT    /{cast_id}        - Update cast member
  DELETE /{cast_id}        - Delete cast member

/ratings
  POST   /                 - Create/update rating
  GET    /user/{user_id}   - User's ratings
  GET    /movie/{movie_id} - Movie's ratings
  PUT    /{rating_id}      - Update rating
  DELETE /{rating_id}      - Delete rating
```

## 🔑 Key Concepts

### Dependency Injection

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def endpoint(db: Session = Depends(get_db)):
    # db is automatically injected
```

### ORM Relationships

```python
# One-to-Many
class User(Base):
    ratings = relationship("Rating", back_populates="user")

# Many-to-Many
class Movie(Base):
    genres = relationship("Genre", secondary=movie_genre)
```

### Schema Validation

```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
```

## ⚡ Quick Tips

1. **Start Simple**: Implement Genre first (no foreign keys)
2. **Test Often**: Use Swagger UI at /docs
3. **Use Migrations**: Always use Alembic for schema changes
4. **Check Logs**: `docker-compose logs` for debugging
5. **Read Examples**: See IMPLEMENTATION_EXAMPLES.md

## 📚 Documentation Files

- `README.md` - Overview and setup
- `PROJECT_OVERVIEW.md` - Architecture details
- `IMPLEMENTATION_EXAMPLES.md` - Code examples
- `SETUP_COMPLETE.md` - This file!
- `src/api/README.md` - API documentation

## 🎓 Learning Path

1. Read PROJECT_OVERVIEW.md
2. Read IMPLEMENTATION_EXAMPLES.md
3. Implement Genre (practice the pattern)
4. Implement User (learn authentication)
5. Implement Movie (learn relationships)
6. Implement Rating (connect everything)
7. Add advanced features

## 🎉 You're Ready to Code!

Start with: `cd src/api && .\setup.ps1`

Then open: http://localhost:5000/docs

Happy coding! 🚀
