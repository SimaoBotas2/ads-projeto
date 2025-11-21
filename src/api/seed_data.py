"""
Seed script to add test movies to the database
Run with: python seed_data.py
"""
from datetime import date
from app.database import SessionLocal, engine, Base
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.director import Director
from app.models.cast import Cast
from app.models.user import User
from app.models.rating import Rating


# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Delete existing data
        print("Cleaning up existing data...")
        db.query(Rating).delete()
        db.query(Movie).delete()
        db.query(User).delete()
        db.query(Cast).delete()
        db.query(Director).delete()
        db.query(Genre).delete()
        db.commit()
        print("✓ Deleted existing data")
        
        print("Seeding database with test data...")
        
        # Create Genres
        action = Genre(name="Action", description="Action-packed movies")
        scifi = Genre(name="Science Fiction", description="Sci-fi movies")
        drama = Genre(name="Drama", description="Dramatic movies")
        thriller = Genre(name="Thriller", description="Thriller movies")
        
        db.add_all([action, scifi, drama, thriller])
        db.commit()
        print("✓ Added genres")
        
        # Create Directors
        nolan = Director(
            name="Christopher Nolan",
            biography="British-American film director known for complex narratives",
            birth_date=date(1970, 7, 30)
        )
        wachowski_lana = Director(
            name="Lana Wachowski",
            biography="American film director and screenwriter",
            birth_date=date(1965, 6, 21)
        )
        wachowski_lilly = Director(
            name="Lilly Wachowski",
            biography="American film director and screenwriter",
            birth_date=date(1967, 12, 29)
        )
        tarantino = Director(
            name="Quentin Tarantino",
            biography="American filmmaker known for nonlinear storylines",
            birth_date=date(1963, 3, 27)
        )
        
        db.add_all([nolan, wachowski_lana, wachowski_lilly, tarantino])
        db.commit()
        print("✓ Added directors")
        
        # Create Cast Members
        dicaprio = Cast(
            name="Leonardo DiCaprio",
            biography="American actor and film producer",
            birth_date=date(1974, 11, 11)
        )
        reeves = Cast(
            name="Keanu Reeves",
            biography="Canadian actor known for action films",
            birth_date=date(1964, 9, 2)
        )
        moss = Cast(
            name="Carrie-Anne Moss",
            biography="Canadian actress",
            birth_date=date(1967, 8, 21)
        )
        travolta = Cast(
            name="John Travolta",
            biography="American actor and singer",
            birth_date=date(1954, 2, 18)
        )
        
        db.add_all([dicaprio, reeves, moss, travolta])
        db.commit()
        print("✓ Added cast members")
        
        # Create Movies
        inception = Movie(
            title="Inception",
            original_title="Inception",
            overview="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            tagline="Your mind is the scene of the crime",
            release_date=date(2010, 7, 16),
            runtime=148,
            budget=160000000,
            revenue=836800000,
            imdb_id="tt1375666",
            original_language="en",
            popularity=85.5,
            vote_average=8.8,
            vote_count=35000,
            genres=[action, scifi, thriller],
            directors=[nolan],
            cast_members=[dicaprio]
        )
        
        matrix = Movie(
            title="The Matrix",
            original_title="The Matrix",
            overview="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            tagline="Welcome to the Real World",
            release_date=date(1999, 3, 31),
            runtime=136,
            budget=63000000,
            revenue=467200000,
            imdb_id="tt0133093",
            original_language="en",
            popularity=92.3,
            vote_average=8.7,
            vote_count=25000,
            genres=[action, scifi],
            directors=[wachowski_lana, wachowski_lilly],
            cast_members=[reeves, moss]
        )
        
        pulp_fiction = Movie(
            title="Pulp Fiction",
            original_title="Pulp Fiction",
            overview="The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            tagline="You won't know the facts until you've seen the fiction",
            release_date=date(1994, 10, 14),
            runtime=154,
            budget=8000000,
            revenue=213900000,
            imdb_id="tt0110912",
            original_language="en",
            popularity=88.7,
            vote_average=8.9,
            vote_count=28000,
            genres=[thriller, drama],
            directors=[tarantino],
            cast_members=[travolta]
        )
        
        interstellar = Movie(
            title="Interstellar",
            original_title="Interstellar",
            overview="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            tagline="Mankind was born on Earth. It was never meant to die here.",
            release_date=date(2014, 11, 7),
            runtime=169,
            budget=165000000,
            revenue=701800000,
            imdb_id="tt0816692",
            original_language="en",
            popularity=91.2,
            vote_average=8.6,
            vote_count=32000,
            genres=[scifi, drama],
            directors=[nolan],
            cast_members=[]
        )
        
        dark_knight = Movie(
            title="The Dark Knight",
            original_title="The Dark Knight",
            overview="When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests to fight injustice.",
            tagline="Why So Serious?",
            release_date=date(2008, 7, 18),
            runtime=152,
            budget=185000000,
            revenue=1005000000,
            imdb_id="tt0468569",
            original_language="en",
            popularity=95.8,
            vote_average=9.0,
            vote_count=40000,
            genres=[action, thriller, drama],
            directors=[nolan],
            cast_members=[]
        )

                # Create Test Users
        user1 = User(
            username="alice",
            email="alice@example.com",
            hashed_password="123"   # se usares hash real, altero isto
        )
        user2 = User(
            username="bob",
            email="bob@example.com",
            hashed_password="123"
        )
        user3 = User(
            username="charlie",
            email="charlie@example.com",
            hashed_password="123"
        )

        db.add_all([user1, user2, user3])
        db.commit()
        print("✓ Added users")

        
        db.add_all([inception, matrix, pulp_fiction, interstellar, dark_knight])
        db.commit()
        print("✓ Added movies")
        
        # Create Ratings
        rating1 = Rating(
            user_id=user1.id,
            movie_id=inception.id,
            rating=9.0,
            review="Mind-bending masterpiece! Nolan really outdid himself."
        )
        rating2 = Rating(
            user_id=user1.id,
            movie_id=matrix.id,
            rating=8.5,
            review="Classic sci-fi action. The effects were groundbreaking for its time."
        )
        rating3 = Rating(
            user_id=user2.id,
            movie_id=pulp_fiction.id,
            rating=9.5,
            review="Tarantino's best work. Brilliant dialogue and storytelling."
        )
        rating4 = Rating(
            user_id=user2.id,
            movie_id=interstellar.id,
            rating=8.8,
            review="Spectacular visuals and emotional depth. A true epic."
        )
        rating5 = Rating(
            user_id=user3.id,
            movie_id=dark_knight.id,
            rating=9.2,
            review="Best superhero film ever made. Ledger's Joker is iconic."
        )
        rating6 = Rating(
            user_id=user3.id,
            movie_id=inception.id,
            rating=8.7,
            review="Great movie, though confusing at times. Worth multiple watches."
        )
        rating7 = Rating(
            user_id=user1.id,
            movie_id=dark_knight.id,
            rating=9.1,
            review="Outstanding performance by the entire cast."
        )
        rating8 = Rating(
            user_id=user2.id,
            movie_id=matrix.id,
            rating=8.3,
            review="Fun action movie. Still holds up pretty well."
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
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
