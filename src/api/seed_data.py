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
        spielberg = Director(
            name="Steven Spielberg",
            nationality="American"
        )
        fincher = Director(
            name="David Fincher",
            nationality="American"
        )
        villeneuve = Director(
            name="Denis Villeneuve",
            nationality="Canadian"
        )
        zemeckis = Director(
            name="Robert Zemeckis",
            nationality="American"
        )
        jackson = Director(
            name="Peter Jackson",
            nationality="New Zealand"
        )
        scorsese = Director(
            name="Martin Scorsese",
            nationality="American"
        )
        
        db.add_all([nolan, wachowski_lana, wachowski_lilly, tarantino, spielberg, 
                    fincher, villeneuve, zemeckis, jackson, scorsese])
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
        tom_hanks = Cast(
            name="Tom Hanks",
            nationality="American"
        )
        morgan_freeman = Cast(
            name="Morgan Freeman",
            nationality="American"
        )
        brad_pitt = Cast(
            name="Brad Pitt",
            nationality="American"
        )
        timothee_chalamet = Cast(
            name="TimothÃ©e Chalamet",
            nationality="American"
        )
        elijah_wood = Cast(
            name="Elijah Wood",
            nationality="American"
        )
        robert_deniro = Cast(
            name="Robert De Niro",
            nationality="American"
        )
        matthew_mcconaughey = Cast(
            name="Matthew McConaughey",
            nationality="American"
        )
        christian_bale = Cast(
            name="Christian Bale",
            nationality="British"
        )
        
        db.add_all([dicaprio, reeves, moss, travolta, tom_hanks, morgan_freeman,
                    brad_pitt, timothee_chalamet, elijah_wood, robert_deniro,
                    matthew_mcconaughey, christian_bale])
        db.commit()
        print("Added cast members")
        
        # Create Movies
        inception = Movie(
            name="Inception",
            description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            launch_date=date(2010, 7, 16),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/10_06/2010/1375666/s_1375666_07030c72.jpg",
            genres=[action, scifi, thriller],
            directors=[nolan],
            cast_members=[dicaprio]
        )
        
        matrix = Movie(
            name="The Matrix",
            description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            launch_date=date(1999, 3, 31),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/06_01/1999/0133093/s_77607_0133093_ab8bc972.jpg",
            genres=[action, scifi],
            directors=[wachowski_lana, wachowski_lilly],
            cast_members=[reeves, moss]
        )
        
        pulp_fiction = Movie(
            name="Pulp Fiction",
            description="The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            launch_date=date(1994, 10, 14),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/25_11/1994/110912/l_pulp-fiction-movie-poster_f099050c.jpg",
            genres=[thriller, drama],
            directors=[tarantino],
            cast_members=[travolta]
        )
        
        interstellar = Movie(
            name="Interstellar",
            description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            launch_date=date(2014, 11, 7),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/14_09/2014/816692/s_816692_593eaeff.jpg",
            genres=[scifi, drama],
            directors=[nolan],
            cast_members=[matthew_mcconaughey]
        )
        
        dark_knight = Movie(
            name="The Dark Knight",
            description="When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests to fight injustice.",
            launch_date=date(2008, 7, 18),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/22_10/2013/11060882/s_batman-the-dark-knight-returns-movie-poster_ac145b01.jpg",
            genres=[action, thriller, drama],
            directors=[nolan],
            cast_members=[christian_bale]
        )
        
        shawshank = Movie(
            name="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            launch_date=date(1994, 9, 23),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/11_08/1994/111161/l_111161_e9ccda65.jpg",
            genres=[drama],
            directors=[],
            cast_members=[morgan_freeman]
        )
        
        forrest_gump = Movie(
            name="Forrest Gump",
            description="The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.",
            launch_date=date(1994, 7, 6),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/12_04/1994/109830/s_109830_58524cd6.jpg",
            genres=[drama],
            directors=[zemeckis],
            cast_members=[tom_hanks]
        )
        
        fight_club = Movie(
            name="Fight Club",
            description="An insomniac office worker and a devil-may-care soap maker form an underground fight club.",
            launch_date=date(1999, 10, 15),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/05_02/1999/0137523/s_7868_0137523_d46e33b9.jpg",
            genres=[drama, thriller],
            directors=[fincher],
            cast_members=[brad_pitt]
        )
        
        dune = Movie(
            name="Dune",
            description="A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions.",
            launch_date=date(2021, 10, 22),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/25_10/2021/1160419/l_dune-part-one-movie-poster_ff9c3c86.jpg",
            genres=[scifi, drama, action],
            directors=[villeneuve],
            cast_members=[timothee_chalamet]
        )
        
        lotr_fellowship = Movie(
            name="The Lord of the Rings: The Fellowship of the Ring",
            description="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring.",
            launch_date=date(2001, 12, 19),
            nationality="New Zealand",
            poster_path="https://posters.movieposterdb.com/22_06/2001/120737/s_120737_0ff31144.jpg",
            genres=[action, drama],
            directors=[jackson],
            cast_members=[elijah_wood]
        )
        
        goodfellas = Movie(
            name="Goodfellas",
            description="The story of Henry Hill and his life in the mob, covering his relationship with his wife and his partners in crime.",
            launch_date=date(1990, 9, 19),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/05_09/1990/0099685/s_54529_0099685_307a5bd2.jpg",
            genres=[drama, thriller],
            directors=[scorsese],
            cast_members=[robert_deniro]
        )
        
        schindlers_list = Movie(
            name="Schindler's List",
            description="In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce.",
            launch_date=date(1993, 12, 15),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/09_02/1993/108052/s_108052_9dd74020.jpg",
            genres=[drama],
            directors=[spielberg],
            cast_members=[]
        )
        
        django = Movie(
            name="Django Unchained",
            description="With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation owner.",
            launch_date=date(2012, 12, 25),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/21_02/2012/1853728/s_1853728_7fb18a9f.jpg",
            genres=[drama, action],
            directors=[tarantino],
            cast_members=[dicaprio]
        )
        
        se7en = Movie(
            name="Se7en",
            description="Two detectives hunt a serial killer who uses the seven deadly sins as his motives.",
            launch_date=date(1995, 9, 22),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/06_05/1995/0114369/s_115148_0114369_f2af901e.jpg",
            genres=[thriller, drama],
            directors=[fincher],
            cast_members=[brad_pitt, morgan_freeman]
        )
        
        saving_private_ryan = Movie(
            name="Saving Private Ryan",
            description="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper.",
            launch_date=date(1998, 7, 24),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/07_10/1998/120815/s_120815_e70398d8.jpg",
            genres=[action, drama],
            directors=[spielberg],
            cast_members=[tom_hanks]
        )

        fight_club = Movie(
            name="Fight Club",
            description="An insomniac office worker and a soap maker form an underground fight club that evolves into something much more dangerous.",
            launch_date=date(1999, 10, 15),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/05_02/1999/0137523/s_7868_0137523_d46e33b9.jpg",
            genres=[drama, thriller],
            directors=[nolan],
            cast_members=[dicaprio],
            avg_rating=4.0,
            count_rating=2
        )

        shawshank = Movie(
            name="The Shawshank Redemption",
            description="Two imprisoned men bond over several years, finding solace and eventual redemption through acts of common decency.",
            launch_date=date(1994, 9, 23),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/11_08/1994/111161/s_111161_e9ccda65.jpg",
            genres=[drama],
            directors=[tarantino],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        mad_max = Movie(
            name="Mad Max: Fury Road",
            description="In a post-apocalyptic wasteland, a drifter and a rebel warrior join forces to escape a tyrannical warlord.",
            launch_date=date(2015, 5, 15),
            nationality="Australia",
            poster_path="https://posters.movieposterdb.com/06_05/1979/0079501/s_115184_0079501_5624763d.jpg",
            genres=[action, thriller],
            directors=[wachowski_lana],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        gladiator = Movie(
            name="Gladiator",
            description="A betrayed Roman general fights his way through the arena seeking vengeance against the corrupt emperor who murdered his family.",
            launch_date=date(2000, 5, 5),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/08_08/2000/172495/s_172495_2cce6a7c.jpg",
            genres=[action, drama],
            directors=[nolan],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        shutter_island = Movie(
            name="Shutter Island",
            description="A U.S. Marshal investigates the disappearance of a murderer from a hospital for the criminally insane.",
            launch_date=date(2010, 2, 19),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/09_08/2009/1130884/s_1130884_84200ccd.jpg",
            genres=[thriller, drama],
            directors=[nolan],
            cast_members=[dicaprio],
            avg_rating=4.0,
            count_rating=2
        )

        john_wick = Movie(
            name="John Wick",
            description="An ex-hitman comes out of retirement to hunt down the gangsters who destroyed everything he had.",
            launch_date=date(2014, 10, 24),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/14_10/2014/2911666/s_2911666_2ba3e7a9.jpg",
            genres=[action, thriller],
            directors=[wachowski_lilly],
            cast_members=[reeves],
            avg_rating=4.0,
            count_rating=2
        )

        the_prestige = Movie(
            name="The Prestige",
            description="Two rival magicians engage in a battle to create the ultimate illusion, pushing the limits of obsession and sacrifice.",
            launch_date=date(2006, 10, 20),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/06_11/2006/0482571/s_146373_0482571_5b8813d5.jpg",
            genres=[thriller, drama],
            directors=[nolan],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        django = Movie(
            name="Django Unchained",
            description="A freed slave teams up with a bounty hunter to rescue his wife from a brutal plantation owner.",
            launch_date=date(2012, 12, 25),
            nationality="USA",
            poster_path="https://www.impawards.com/2012/django_unchained_ver8_xlg.jpg",
            genres=[action, drama],
            directors=[tarantino],
            cast_members=[travolta],
            avg_rating=4.0,
            count_rating=2
        )

        arrival = Movie(
            name="Arrival",
            description="A linguist is recruited to communicate with extraterrestrial visitors, uncovering a mystery that transcends time.",
            launch_date=date(2016, 11, 11),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/14_02/2013/3404240/s_3404240_8c5a4155.jpg",
            genres=[scifi, drama],
            directors=[nolan],
            cast_members=[],
            avg_rating=4.0,
            count_rating=2
        )

        blade_runner = Movie(
            name="Blade Runner 2049",
            description="A young blade runner discovers a long-buried secret that threatens to plunge what's left of society into chaos.",
            launch_date=date(2017, 10, 6),
            nationality="USA",
            poster_path="https://posters.movieposterdb.com/22_11/1997/126817/s_blade-runner-movie-poster_144d650e.jpg",
            genres=[scifi, thriller],
            directors=[wachowski_lana],
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

        db.add_all([inception, matrix, pulp_fiction, interstellar, dark_knight, fight_club, shawshank, mad_max, gladiator, shutter_island, john_wick, the_prestige, django, arrival, blade_runner, dune, lotr_fellowship, forrest_gump, goodfellas, schindlers_list, se7en, saving_private_ryan])
        db.commit()
        print("Added movies")
        
        # Create Ratings (evaluation must be 1-4)
        ratings = [
            # User 1 ratings
            Rating(user_id=user1.id, movie_id=inception.id, evaluation=4),
            Rating(user_id=user1.id, movie_id=matrix.id, evaluation=4),
            Rating(user_id=user1.id, movie_id=dark_knight.id, evaluation=4),
            Rating(user_id=user1.id, movie_id=interstellar.id, evaluation=4),
            Rating(user_id=user1.id, movie_id=fight_club.id, evaluation=4),
            Rating(user_id=user1.id, movie_id=dune.id, evaluation=3),
            Rating(user_id=user1.id, movie_id=lotr_fellowship.id, evaluation=4),
            
            # User 2 ratings
            Rating(user_id=user2.id, movie_id=pulp_fiction.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=interstellar.id, evaluation=3),
            Rating(user_id=user2.id, movie_id=matrix.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=shawshank.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=forrest_gump.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=goodfellas.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=se7en.id, evaluation=4),
            Rating(user_id=user2.id, movie_id=saving_private_ryan.id, evaluation=4),
            
            # User 3 ratings
            Rating(user_id=user3.id, movie_id=dark_knight.id, evaluation=4),
            Rating(user_id=user3.id, movie_id=inception.id, evaluation=3),
            Rating(user_id=user3.id, movie_id=pulp_fiction.id, evaluation=4),
            Rating(user_id=user3.id, movie_id=schindlers_list.id, evaluation=4),
            Rating(user_id=user3.id, movie_id=django.id, evaluation=3),
            Rating(user_id=user3.id, movie_id=fight_club.id, evaluation=4),
            Rating(user_id=user3.id, movie_id=lotr_fellowship.id, evaluation=4),
            Rating(user_id=user3.id, movie_id=dune.id, evaluation=3),
            Rating(user_id=user3.id, movie_id=forrest_gump.id, evaluation=3),
            Rating(user_id=user3.id, movie_id=saving_private_ryan.id, evaluation=4),
        ]
        
        db.add_all(ratings)
        db.commit()
        print("✓ Added ratings")
        
        # Update avg_rating and count_rating for each movie
        print("Calculating movie ratings...")
        movies = db.query(Movie).all()
        for movie in movies:
            movie_ratings = db.query(Rating).filter(Rating.movie_id == movie.id).all()
            if movie_ratings:
                movie.count_rating = len(movie_ratings)
                movie.avg_rating = sum(r.evaluation for r in movie_ratings) / len(movie_ratings)
            else:
                movie.count_rating = 0
                movie.avg_rating = None
        db.commit()
        print("✓ Updated movie ratings")
        
        print(f"\n✓ Successfully seeded database with:")
        print(f"   - 4 genres")
        print(f"   - 10 directors")
        print(f"   - 12 cast members")
        print(f"   - 3 users")
        print(f"   - 15 movies")
        print(f"   - {len(ratings)} ratings")
        print(f"\nYou can now test the API at http://localhost:5000/docs")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
    print("Seeding finished.")
