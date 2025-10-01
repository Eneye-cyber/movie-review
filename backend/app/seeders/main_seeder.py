from app.seeders.user_seeder import UserSeeder
from app.seeders.movie_seeder import MovieSeeder
from app.seeders.rating_seeder import RatingSeeder
import time

class MainSeeder:
    def __init__(self):
        self.user_seeder = UserSeeder()
        self.movie_seeder = MovieSeeder()
        self.rating_seeder = RatingSeeder()
    
    def run(self, user_count=20, movie_count=50, ratings_per_movie=5):
        print("Starting database seeding...")
        start_time = time.time()
        
        try:
            # Seed users
            users = self.user_seeder.run(user_count)
            
            # Seed movies
            movies = self.movie_seeder.run(users, movie_count)
            
            # Seed ratings
            ratings = self.rating_seeder.run(users, movies, ratings_per_movie)
            
            elapsed_time = time.time() - start_time
            print(f"Seeding completed in {elapsed_time:.2f} seconds!")
            print(f"Summary: {len(users)} users, {len(movies)} movies, {len(ratings)} ratings")
            
            # Print some test credentials
            print("\nTest User Credentials:")
            print("Username: admin, Password: Admin123!")
            print("Username: john_doe, Password: Password123!")
            print("Username: jane_smith, Password: Password123!")
            
        except Exception as e:
            print(f"Seeding failed: {e}")
            raise
        finally:
            self.user_seeder.close()
            self.movie_seeder.close()
            self.rating_seeder.close()