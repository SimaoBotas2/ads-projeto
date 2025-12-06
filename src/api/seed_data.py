"""
Seed script to add test movies to the database
Run with: python seed_data.py
"""
from datetime import date
import hashlib
import os
import sys
from app.database import SessionLocal
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.director import Director
from app.models.cast import Cast
from app.models.user import User
from app.models.rating import Rating


def hash_password(password: str) -> str:
    """Hash password with salt for seed data"""
    salt = os.urandom(16)
    salt_hex = salt.hex()
    hash_hex = hashlib.sha256(salt + password.encode()).hexdigest()
    return f"{salt_hex}:{hash_hex}"

# NOTE: Do NOT drop or create tables here. Use alembic migrations to manage schema.
print("Seeding script started. Ensure migrations have already been applied (alembic upgrade head).")

def seed_database():
    db = SessionLocal()
    
    try:
        # If there is already movie data, assume DB has been seeded/migrated and skip.
        existing = db.query(Movie).first()
        if existing:
            print("Database already contains data; skipping seeding.")
            return

        # Delete existing data
        print("Cleaning up any partial data (ratings only)...")
        # Only remove ratings to avoid destructive operations in production
        db.query(Rating).delete()
        db.commit()
        print("Deleted existing ratings")
        
        print("Seeding database with test data...")
        
        # Create Genres
        action = Genre(name="Action")
        scifi = Genre(name="Science Fiction")
        drama = Genre(name="Drama")
        thriller = Genre(name="Thriller")
        
        db.add_all([action, scifi, drama, thriller])
        db.commit()
        print("Added genres")
        
        # Create Directors
        nolan = Director(
            name="Christopher Nolan",
            nationality="British-American"
        )
        wachowski_lana = Director(
            name="Lana Wachowski",
            nationality="American"
        )
        wachowski_lilly = Director(
            name="Lilly Wachowski",
            nationality="American"
        )
        tarantino = Director(
            name="Quentin Tarantino",
            nationality="American"
        )
        
        db.add_all([nolan, wachowski_lana, wachowski_lilly, tarantino])
        db.commit()
        print("Added directors")
        
        # Create Cast Members
        dicaprio = Cast(
            name="Leonardo DiCaprio",
            nationality="American"
        )
        reeves = Cast(
            name="Keanu Reeves",
            nationality="Canadian"
        )
        moss = Cast(
            name="Carrie-Anne Moss",
            nationality="Canadian"
        )
        travolta = Cast(
            name="John Travolta",
            nationality="American"
        )
        
        db.add_all([dicaprio, reeves, moss, travolta])
        db.commit()
        print("Added cast members")
        
        # Create Movies
        inception = Movie(
            name="Inception",
            description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            launch_date=date(2010, 7, 16),
            nationality="USA",
            poster_path="/inception_poster.jpg",
            genres=[action, scifi, thriller],
            directors=[nolan],
            cast_members=[dicaprio],
            avg_rating=4.0,
            count_rating=2
        )
        
        matrix = Movie(
            name="The Matrix",
            description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            launch_date=date(1999, 3, 31),
            nationality="USA",
            poster_path="/matrix_poster.jpg",
            genres=[action, scifi],
            directors=[wachowski_lana, wachowski_lilly],
            cast_members=[reeves, moss],
            avg_rating=4.0,
            count_rating=2
        )
        
        pulp_fiction = Movie(
            name="Pulp Fiction",
            description="The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            launch_date=date(1994, 10, 14),
            nationality="USA",
            poster_path="/pulp_fiction_poster.jpg",
            genres=[thriller, drama],
            directors=[tarantino],
            cast_members=[travolta],
            avg_rating=4.0,
            count_rating=1
        )
        
        interstellar = Movie(
            name="Interstellar",
            description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            launch_date=date(2014, 11, 7),
            nationality="USA",
            poster_path="/interstellar_poster.jpg",
            genres=[scifi, drama],
            directors=[nolan],
            cast_members=[],
            avg_rating=4.0,
            count_rating=1
        )
        
        dark_knight = Movie(
            name="The Dark Knight",
            description="When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests to fight injustice.",
            launch_date=date(2008, 7, 18),
            nationality="USA",
            poster_path="/dark_knight_poster.jpg",
            genres=[action, thriller, drama],
            directors=[nolan],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        # Create Test Users
        user1 = User(
            username="alice",
            email="alice@example.com",
            name="Alice Smith",
            password=hash_password("password123")
        )
        user2 = User(
            username="bob",
            email="bob@example.com",
            name="Bob Johnson",
            password=hash_password("password123")
        )
        user3 = User(
            username="charlie",
            email="charlie@example.com",
            name="Charlie Brown",
            password=hash_password("password123")
        )

        db.add_all([user1, user2, user3])
        db.commit()
        print("Added users")

        
        db.add_all([inception, matrix, pulp_fiction, interstellar, dark_knight])
        db.commit()
        print("Added movies")
        
        # Create Ratings (evaluation must be 1-4)
        rating1 = Rating(
            user_id=user1.id,
            movie_id=inception.id,
            evaluation=4
        )
        rating2 = Rating(
            user_id=user1.id,
            movie_id=matrix.id,
            evaluation=4
        )
        rating3 = Rating(
            user_id=user2.id,
            movie_id=pulp_fiction.id,
            evaluation=4
        )
        rating4 = Rating(
            user_id=user2.id,
            movie_id=interstellar.id,
            evaluation=4
        )
        rating5 = Rating(
            user_id=user3.id,
            movie_id=dark_knight.id,
            evaluation=4
        )
        rating6 = Rating(
            user_id=user3.id,
            movie_id=inception.id,
            evaluation=4
        )
        rating7 = Rating(
            user_id=user1.id,
            movie_id=dark_knight.id,
            evaluation=4
        )
        rating8 = Rating(
            user_id=user2.id,
            movie_id=matrix.id,
            evaluation=4
        )
        
        db.add_all([rating1, rating2, rating3, rating4, rating5, rating6, rating7, rating8])
        db.commit()
        print("✓ Added ratings")
        
        print(f"\n✅ Successfully seeded database with:")
        print(f"   - 4 genres")
        print(f"   - 4 directors")
        print(f"   - 4 cast members")
        print(f"   - 3 users")
        print(f"   - 5 movies")
        print(f"   - 8 ratings")
        print(f"\nYou can now test the API at http://localhost:5000/docs")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
    print("Seeding finished.")
